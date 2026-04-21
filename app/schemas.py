from pydantic import BaseModel


class PostCreate(BaseModel):
    name: str
    skill: str
    id: int
