from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class App(BaseModel):
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
    hosts: list
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
        from_attributes = True


class AppCreate(App):
    name: str
    services: list
    command: Optional[str] = None
    ports: Optional[list] = None
    volumes: Optional[list] = None
    labels: Optional[list] = None
    scale: Optional[int] = None
    image: Optional[str] = None
    network: Optional[str] = None
    hosts: Optional[list] = None
    ip: Optional[str] = None
    port: Optional[str] = None
    count: Optional[int] = None
    environment: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[str] = None


class ServiceUpdate(App):
    pass


class ServiceDelete(App):
    pass


class UserBase(BaseModel):
    id: Optional[int]
    services: list


class UserCreate(BaseModel):
    full_name: Optional[str]
    email: str
    password: str


class UserUpdate(UserBase):
    password: str
    is_active: bool


class User(UserBase):
    id: int
    is_active: bool
    services: list[App] = []

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class OPAConfigBase(BaseModel):
    threshold: int
    policy_status: str
    policy: str


class OPAConfigCreate(OPAConfigBase):
    pass


class OPAConfigUpdate(OPAConfigBase):
    pass


class OPAConfigInDB(OPAConfigBase):
    id: int

    class Config:
        from_attributes = True
