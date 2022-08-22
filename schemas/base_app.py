from typing import Optional
from pydantic import BaseModel

class BaseApp(BaseModel):
    id: Optional[int]
    image: str
    name: str

