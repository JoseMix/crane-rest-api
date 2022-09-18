from typing import Optional

from pydantic import BaseModel

class App(BaseModel):
    id: Optional[str]
    name: Optional[str]
    services: Optional[list]
    command: Optional[str]
    ports: Optional[list]
    volumes: Optional[list]
    labels: Optional[list]
    scale: Optional[int]
    image: Optional[str]
    network: Optional[str]
    ip: Optional[str]
    port: Optional[str]
    count: Optional[int]
    environment: Optional[str]
    status: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]
    user_id: Optional[int]
    

