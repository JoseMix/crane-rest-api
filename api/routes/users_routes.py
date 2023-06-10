from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.db.crud import get_users, create_user, get_user, create_user_app, get_services
from api.db.schemas import UserCreate

userRouter = APIRouter()

@userRouter.post("/")
def create(user, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@userRouter.get("/")
def get(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db=db, skip=skip, limit=limit)


@userRouter.get("/{user_id}")
def get_by_id(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)


@userRouter.post("/{user_id}/services/")
def create_service(user_id: int, service, db: Session = Depends(get_db)):
    return create_user_app(db, user_id, service)


@ userRouter.get("/services/")
def get_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_services(db, skip, limit)
