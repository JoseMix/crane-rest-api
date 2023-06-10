from typing import Optional
from pydantic import BaseModel


class App(BaseModel):
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
