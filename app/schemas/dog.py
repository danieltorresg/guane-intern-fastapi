from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseDog(BaseModel):
    id: int
    owner_id: Optional[int]

class CreateDog(BaseDog):
    name: str
    picture: str

class UpdateDog(BaseModel):
    picture: Optional[str]
    is_adopted: Optional[bool]
    owner_id: Optional[int]


class DogInDB(CreateDog):
    created_date: datetime
    is_adopted: bool


class Dog(DogInDB):
    pass
