package rbac.authz

import rego.v1

role_permissions := {
    "ADMIN": [
        {"action": "GET",  "object": "APPS"},
        {"action": "POST",  "object": "APPS"},
        {"action": "PATCH",  "object": "APPS"},
        {"action": "DELETE",  "object": "APPS"},
        {"action": "GET",  "object": "ROLES"},
        {"action": "POST",  "object": "ROLES"},
        {"action": "PATCH",  "object": "ROLES"},
        {"action": "DELETE",  "object": "ROLES"},
        {"action": "GET",  "object": "OPA"},
        {"action": "POST",  "object": "OPA"},
        {"action": "PATCH",  "object": "OPA"},
        {"action": "DELETE",  "object": "OPA"},
        {"action": "GET",  "object": "MONITORING"},
        {"action": "POST",  "object": "MONITORING"},
        {"action": "PATCH",  "object": "MONITORING"},
        {"action": "DELETE",  "object": "MONITORING"}
    ],
    "USER":  [{"action": "GET",  "object": "APPS"}],
}

# logic that implements RBAC.
default allow := false
allow if {
    # lookup the list of roles for the user
    roles := input.roles

    # for each role in that list
    r := roles[_]

    # lookup the permissions list for role r
    permissions := role_permissions[r]

    # for each permission
    p := permissions[_]

    # check if the permission granted to r matches the user's request
    p == {"action": input.action, "object": input.object}
}