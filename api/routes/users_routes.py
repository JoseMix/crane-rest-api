from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db.database import get_db
import api.db.crud.user_crud as UserRepository
from api.db.schemas import UserCreate

userRouter = APIRouter()


@userRouter.post("/")
def create(user, db: Session = Depends(get_db)):
    return UserRepository.register(db=db, user=user)


@userRouter.get("/")
def get(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return UserRepository.get_all(db=db, skip=skip, limit=limit)


@userRouter.get("/{user_id}")
def get_by_id(user_id: int, db: Session = Depends(get_db)):
    return UserRepository.get_by_id(db, user_id)
