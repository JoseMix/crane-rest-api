''' 
Utilizando el userId que obtiene del JWT debe:
- Obtener los roles del usuario de la base de datos
- Actualizar el roles.rego con los roles del usuario ej:
user_roles := {
    "franco@gmail.com": ["ADMIN", "USER"],
}
- Realizar la consulta de la politica con el nuevo user_roles usando el nombre de la ruta y el metodo HTTP ej:

"input": {
            "email": "franco@gmail.com",
            "action": "read",
            "object": "database456"
}
'''


from fastapi import HTTPException
from sqlalchemy.orm import Session
import api.db.crud.role_crud as RoleCrud
from api.schemas.user import User
from api.clients.OPAClient import test, get_policies, update_policies_file, check_policy, create_opa_policy, update_or_create_opa_data
from api.config.constants import *
from typing import List
import json
import uuid
import re


async def verify(db: Session, db_user: User, route: str, method: str):
    roles = RoleCrud.get_roles_by_user(db, db_user)
    user_roles = {db_user.email: [role.name for role in roles]}
    update_or_create_opa_data(user_roles, "rbac/user_roles")
    input_data = {
        "input": {
            "user": db_user.email,
            "action": method,
            "object": route
        }
    }
    return check_policy("rbac", "allow", input_data)
