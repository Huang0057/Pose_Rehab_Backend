from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    """
    用於註冊的請求模型
    只需要用戶名和密碼
    """
    username: str = Field(..., min_length=1, max_length=50)  
    password: str = Field(..., min_length=6)  

class UserResponse(BaseModel):
    """
    用於返回用戶資訊的響應模型
    不包含密碼，但包含 uid 和 coins
    """
    username: str
    uid: str
    coins: int

    class Config:
        orm_mode = True