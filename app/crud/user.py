from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import User
from app.schemas.user import UserCreate
from app.database import database

# 設置密碼雜湊上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_username(username: str):
    """根據用戶名查詢用戶"""
    query = f"""
    SELECT * FROM users WHERE username = :username
    """
    return await database.fetch_one(query=query, values={"username": username})

async def create_user(user: UserCreate):
    """創建新用戶"""
    # 對密碼進行雜湊處理
    hashed_password = pwd_context.hash(user.password)
    
    # 創建用戶（讓資料庫自動生成 uid）
    query = """
    INSERT INTO users (username, password)
    VALUES (:username, :password)
    RETURNING *
    """
    values = {
        "username": user.username,
        "password": hashed_password
    }
    
    # 執行插入操作並獲取結果
    created_user = await database.fetch_one(query=query, values=values)
    
    # 返回創建的用戶資訊
    return {
        "username": created_user.username,
        "uid": created_user.uid,
        "coins": created_user.coins
    }

async def verify_password(plain_password: str, hashed_password: str):
    """驗證密碼"""
    return pwd_context.verify(plain_password, hashed_password)