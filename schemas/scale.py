from pydantic import BaseModel

class Scale(BaseModel):
    name: str
    count: int

