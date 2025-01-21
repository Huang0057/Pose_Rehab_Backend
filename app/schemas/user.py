from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    uid: str
    coins: int

    class Config:
        from_attributes = True