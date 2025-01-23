from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import User
from app.database import database

# 設置密碼雜湊上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(username: str, password: str):
    hashed_password = pwd_context.hash(password)
    query = """
    INSERT INTO users (username, password)
    VALUES (:username, :password)
    RETURNING *
    """
    values = {"username": username, "password": hashed_password}
    return await database.fetch_one(query=query, values=values)

async def verify_password(plain_password: str, hashed_password: str):
    """驗證密碼"""
    return pwd_context.verify(plain_password, hashed_password)

async def verify_user(username: str, password: str):
    query = """
    SELECT * FROM users WHERE username = :username
    """
    user = await database.fetch_one(query=query, values={"username": username})
    
    if not user:
        return None
        
    if not pwd_context.verify(password, user.password):
        return None
        
    return user