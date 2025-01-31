from pydantic import BaseModel, Field
from typing import Optional


class UserRegister(BaseModel):

    username: str = Field(..., min_length=1, max_length=50)
    password: str 

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):

    username: str
    uid: str
    coins: int
    streak_days:int
    token: Optional[str] = None
    
    class Config:
        
        from_attributes = True  

