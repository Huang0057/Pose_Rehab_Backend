from pydantic import BaseModel, Field

class UserCreate(BaseModel):

    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):

    username: str
    uid: str
    coins: int

    class Config:
        
        from_attributes = True  