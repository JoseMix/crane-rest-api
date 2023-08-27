from opa_client.opa import OpaClient
from api.db.models import OPAConfig
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


def check_policy(policy_name, rule_name, input_data):
    """
    Check a given policy with provided input data.
    """
    opa_client = get_opa_client()
    response = opa_client.check_permission(
        input_data=input_data, policy_name=policy_name, rule_name=rule_name
    )

    if 'result' in response:
        return response['result']
    raise HTTPException(status_code=404, detail="Policy decision not found")


def create_policy(policy_name, policy_content):
    """
    Print and create a policy.
    """
    return update_policy(policy_name, policy_content)


def update_policy(policy_name, policy_content):
    """
    Update an existing policy or create a new one if it doesn't exist.
    """
    opa_client = get_opa_client()
    return opa_client.update_opa_policy_fromstring(policy_content, policy_name)


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
    update_policy(config.policy_name, policy_content)

    # Verify access for a user
    print(check_policy(config.policy_name, {"input": {"role": "admin"}}))
    print(check_policy(config.policy_name, {"input": {"role": "user"}}))

    return config


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
