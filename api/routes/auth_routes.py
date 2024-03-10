import jwt
import os
from fastapi import Depends, APIRouter, HTTPException, Header, Request
from sqlalchemy.orm import Session
from api.db import models, schemas
from api.db.database import engine, get_db
from api.config.constants import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_TIME_MINUTES, API_PREFIX
import api.db.crud.user_crud as UserRepository
from api.db.crud.role_crud import get_roles_by_user
from api.clients.OPAClient import update_or_create_opa_data, check_policy


models.Base.metadata.create_all(bind=engine)

authRouter = APIRouter()


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
    roles = get_roles_by_user(db, db_user)
    user_roles = {db_user.email: [role.name for role in roles]}

    # Get the current path and method
    path = request.url.path
    method = request.method
    is_allowed = await verify_permissions(db_user.email, user_roles, path, method)
    if not is_allowed:
        raise HTTPException(status_code=403, detail="Forbidden")

    return db_user


async def verify_permissions(email: str, user_roles: dict, route: str, method: str):
    route = route.split("/api")[1]
    route = route.split("/")[2]
    print("Verifying permissions", email, route, method)
    update_or_create_opa_data(user_roles, "rbac/user_roles")
    input_data = {
        "input": {
            "user": email,
            "action": method,
            "object": route.upper()
        }
    }
    return check_policy("rbac", "allow", input_data).get("result")


@authRouter.post("/login", tags=["auth"], description="Login to get an authentication token")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = UserRepository.login(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT
    payload = {"user_id": db_user.id}
    access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token":  access_token, "token_type": "bearer", "expires_in": JWT_EXPIRATION_TIME_MINUTES}


@authRouter.post("/register", tags=["auth"], description="Register a new user")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = UserRepository.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = UserRepository.register(db=db, user=user)
    return {"message": "User created successfully"}
