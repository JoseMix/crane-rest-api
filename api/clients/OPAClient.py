import requests
from fastapi import HTTPException
from opa_client.opa import OpaClient

OPA_SERVER_URL = "http://localhost:8181"


def check_connection():
    try:
        opa_client = OpaClient()
        if opa_client.check_connection():
            return opa_client
        else:
            raise HTTPException(
                status_code=404, detail="OPA server is not running")
    except:
        raise HTTPException(
            status_code=404, detail="OPA server is not running")


def check_policy(POLICY_NAME):
    opa_client = check_connection()
    url = f"{OPA_SERVER_URL}/v1/data/{POLICY_NAME}/allow"
    response = opa_client.get_policies_list()
    print(response)
    return response


def create_policy(POLICY_NAME):
    opa_client = OpaClient()
    url = f"{OPA_SERVER_URL}/v1/policies/{POLICY_NAME}"
    opa_client.update_opa_policy_fromfile(url, input_data)
