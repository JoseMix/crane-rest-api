import jwt
import os
from fastapi import Depends, APIRouter, HTTPException, Header, Request
from sqlalchemy.orm import Session
from api.db import models, schemas
from api.db.database import engine, get_db
from api.config.constants import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_TIME_MINUTES, API_PREFIX, OPA_RBAC_CONFIG_NAME, OPA_RBAC_RULE_NAME
import api.db.crud.user_crud as UserRepository
from api.db.crud.role_crud import get_roles_by_user
from api.clients.OPAClient import update_or_create_opa_data, check_policy


models.Base.metadata.create_all(bind=engine)
authRouter = APIRouter()


@authRouter.post("/login", tags=["auth"], description="Login to get an authentication token")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = UserRepository.login(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Get user roles
    roles = get_roles_by_user(db, db_user)
    user_roles = {db_user.email: [role.name for role in roles]}
    update_or_create_opa_data(user_roles, f"rbac/user_roles/{db_user.email}")

    # Generate JWT
    payload = {"user_id": db_user.id, "email": db_user.email,
               "roles": user_roles.get(db_user.email)}
    access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token":  access_token, "token_type": "bearer", "expires_in": JWT_EXPIRATION_TIME_MINUTES}


@authRouter.post("/register", tags=["auth"], description="Register a new user")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = UserRepository.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = UserRepository.register(db=db, user=user)
    return {"message": "User created successfully"}


def decode_token(token: str, jwt_secret: str, jwt_algorithm: str):
    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
        return payload
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def verify_jwt(request: Request, Authorization: str = Header(...), db: Session = Depends(get_db)):
    payload = decode_token(Authorization, JWT_SECRET, JWT_ALGORITHM)
    user_id = payload.get("user_id")
    db_user = UserRepository.get_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid user")
    is_allowed = await verify_permissions(db_user.email, payload.get("roles"), request.url.path, request.method)
    if not is_allowed:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db_user


async def verify_permissions(email: str, roles: list, route: str, method: str):
    route = route.split("/api")[1]
    route = route.split("/")[2]
    input_data = {
        "input": {
            "roles": roles,
            "action": method,
            "object": route.upper()
        }
    }
    return check_policy(OPA_RBAC_CONFIG_NAME, OPA_RBAC_RULE_NAME, input_data).get("result")
