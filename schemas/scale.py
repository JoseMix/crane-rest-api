from pydantic import BaseModel

class Scale(BaseModel):
    id: str
    count: int

