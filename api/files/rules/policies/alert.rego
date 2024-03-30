package rbac.authz

import rego.v1

alert_action := {
    "service_down": [
        {"status": "firing",  "action": "restart"},
        {"status": "resolved",  "action": "none"},        
    ],
    "high_request_count": [
        {"status": "firing",  "action": "scale"},
        {"status": "resolved",  "action": "deescalate"},        
    ],
}





   