from pydantic import BaseModel
from typing import Optional


class Service(BaseModel):
    id: str
    name: str
    services: list
    command: str
    ports: list
    volumes: list
    labels: list
    scale: int
    image: str
    network: str
    ip: str
    port: str
    count: int
    environment: str
    status: str
    created_at: str
    updated_at: str
    deleted_at: str
    user_id: int

    class Config:
        orm_mode = True


class ServiceCreate(Service):
    name: str
    services: list
    command: Optional[str] = None
    ports: Optional[list] = None
    volumes: Optional[list] = None
    labels: Optional[list] = None
    scale: Optional[int] = None
    image: Optional[str] = None
    network: Optional[str] = None
    ip: Optional[str] = None
    port: Optional[str] = None
    count: Optional[int] = None
    environment: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    deleted_at: Optional[str] = None
    user_id: Optional[int] = None


class ServiceUpdate(Service):
    pass


class ServiceDelete(Service):
    pass


class UserBase(BaseModel):
    id: Optional[int]
    full_name: Optional[str]
    email: str
    is_active: bool
    services: list


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    services: list[Service] = []
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str
