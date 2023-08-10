import requests
from fastapi import HTTPException
from opa_client.opa import OpaClient

OPA_SERVER_URL = "http://localhost:8181"
POLICY_NAME = "default-policy"


def check_policy(input_data):
    opa_client = OpaClient()
    if opa_client.check_connection():
        print("OPA server is up and running")
    else:
        print("OPA server is not running")
    breakpoint()
    result = opa_client.update_opa_policy_fromstring("""
...     package play
... 
...     import data.testapi.testdata
... 
...     default hello = false
... 
...     hello {
...         m := input.message
...         testdata[i] == m
...     }
... """, POLICY_NAME)
    if not result["result"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return True


def create_policy(input_data):
    opa_client = OpaClient()
    url = f"{OPA_SERVER_URL}/v1/policies/{POLICY_NAME}"
    opa_client.update_opa_policy_fromfile(url, input_data)
