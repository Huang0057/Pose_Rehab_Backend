from passlib.context import CryptContext
from ..models.base import users
from ..schemas.user import UserCreate
from ..database import database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_username(username: str):
    """根據用戶名查詢用戶"""
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)

async def create_user(user: UserCreate):
    """創建新用戶"""
    # 雜湊處理
    hashed_password = pwd_context.hash(user.password)
    
    # 創建用戶 
    query = users.insert().values(
        username=user.username,
        password=hashed_password
    )
    
    user_id = await database.execute(query)
    
    # 查詢創建的用戶資訊
    query = users.select().where(users.c.id == user_id)
    created_user = await database.fetch_one(query)
    
    return {
        "username": created_user.username,
        "uid": created_user.uid,
        "coins": created_user.coins
    }

async def verify_password(plain_password: str, hashed_password: str):
    """驗證密碼"""
    return pwd_context.verify(plain_password, hashed_password)