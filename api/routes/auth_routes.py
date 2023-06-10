import jwt
import os
from fastapi import Depends, APIRouter, HTTPException, Header
from sqlalchemy.orm import Session
from api.db import crud, models, schemas
from api.db.database import engine, get_db

models.Base.metadata.create_all(bind=engine)
JWT_SECRET = os.getenv("JWT_SECRET") or "secret"
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM") or "HS256"
JWT_EXPIRATION_TIME_MINUTES = int(
    os.getenv("JWT_EXPIRATION_TIME_MINUTES") or 15)
authRouter = APIRouter()


def decode_token(token: str, jwt_secret: str, jwt_algorithm: str):
    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
        return payload
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def verify_jwt(Authorization: str = Header(...), db: Session = Depends(get_db)):
    payload = decode_token(Authorization, JWT_SECRET, JWT_ALGORITHM)
    user_id = payload.get("user_id")
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid user")
    return db_user


@authRouter.post("/login", tags=["auth"], description="Login to get an authentication token")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.login_user(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT
    payload = {"user_id": db_user.id}
    access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token":  access_token, "token_type": "bearer"}


@authRouter.post("/register", tags=["auth"], description="Register a new user")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
