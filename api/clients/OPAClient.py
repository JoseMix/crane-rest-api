from opa_client.opa import OpaClient
from api.db.models import OPAConfig,OPAStatic
from fastapi import HTTPException
import os

OPA_SERVER_URL = "http://localhost:8181"


def get_opa_client():
    """
    Establish a connection with the OPA server.
    """
    opa_client = OpaClient()
    if opa_client.check_connection() != "Yes I'm here :)":
        raise HTTPException(
            status_code=404, detail="OPA server is not running"
        )
    return opa_client


def get_policies():
    """
    Fetch all available policies.
    """
    opa_client = get_opa_client()
    return opa_client.get_policies_list()


def check_policy(policy_status, rule_name, input_data):
    """
    Check a given policy with provided input data.
    """
    opa_client = get_opa_client()
    response = opa_client.check_permission(
        input_data=input_data, policy_status=policy_status, rule_name=rule_name
    )

    if 'result' in response:
        return response['result']
    raise HTTPException(status_code=404, detail="Policy decision not found")


def create_policy(policy_status, policy_content):
    """
    Print and create a policy.
    """
    return update_policy(policy_status, policy_content)


def update_policy(policy_status, policy_content):
    """
    Update an existing policy or create a new one if it doesn't exist.
    """
    opa_client = get_opa_client()
    return opa_client.update_opa_policy_fromstring(policy_content, policy_status)


def delete_all_policies():
    """
    Delete all policies from OPA.
    """
    opa_client = get_opa_client()
    policies_list = opa_client.get_policies_list()
    for policy in policies_list:
        opa_client.delete_opa_policy(policy)
    return "All policies deleted successfully!"


def test(db, opaConfig):
    """
    Test functionality to create a policy, update it, and check access.
    """
    # Delete all policies from OPA
    delete_all_policies()

    # Create the configuration in the database
    # Assuming 'create_config' is a function you already have
    config = create_config(db, opaConfig)

    # Load the policy content from the given path
    path = os.path.abspath("api/config/policy.rego")

    with open(path) as policy_file:
        policy_content = policy_file.read()

    # Update the policy in OPA with the loaded content
    update_policy(config.policy_status, policy_content)

    # Verify access for a user
    print(check_policy(config.policy_status, 'allow', {"input": {"role": "admin"}}))
    print(check_policy(config.policy_status, 'allow',{"input": {"role": "user"}}))

    return config


def update_policies_file(db):
    configs = db.query(OPAConfig.policy_status,OPAConfig.policy).all()
    static_config = db.query(OPAStatic.package,OPAStatic.default_status).all()
    write_policies(configs,static_config)

def write_policies(policies,static_config):
    rego_path = os.path.abspath("api/config/policy.rego")
    try:
        with open(rego_path,'w') as file:
            for default_status,package in static_config:
                file.write(default_status+"\n\n")
                file.write(package+"\n\n")
            for policy_status,policy_item in policies:
                policy = policy_item
                file.write(policy_status+"\n\n")
                file.write(policy + "\n\n")
    except Exception as error:
        print(f"An error occurred while writing the file: {str(error)}")

def get_configs_from_db(db):
    configs = db.query(OPAConfig).all()
    configs.opa_policy = get_policies()
    if configs:
        return configs
    raise HTTPException(
        status_code=404, detail="Configurations not found in the database"
    )


def create_config(db, opaConfig):
    config = OPAConfig(**opaConfig.dict())
    db.add(config)
    db.commit()
    db.refresh(config)
    return config
