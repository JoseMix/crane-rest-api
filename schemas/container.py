from typing import Optional
from pydantic import BaseModel

class Container (BaseModel):
    id: Optional[str]
    name: Optional[str]