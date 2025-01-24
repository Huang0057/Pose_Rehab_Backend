from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import User
from app.database import database
from sqlalchemy import func, and_
from datetime import datetime, timedelta

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

async def get_streak_days(uid: str):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    query = """
    WITH RECURSIVE streak AS (
        SELECT checkin_date
        FROM user_checkin
        WHERE user_uid = :uid 
        AND checkin_date = :yesterday
        AND signed_in = true
        
        UNION ALL
        
        SELECT c.checkin_date
        FROM user_checkin c
        INNER JOIN streak s ON c.checkin_date = s.checkin_date - INTERVAL '1 day'
        WHERE c.user_uid = :uid AND c.signed_in = true
    )
    SELECT COUNT(*) FROM streak
    """
    
    result = await database.fetch_val(
        query=query, 
        values={"uid": uid, "yesterday": yesterday}
    )
    return result + 1 

async def get_user_by_id(uid: str):
   query = "SELECT * FROM users WHERE uid = :uid"
   return await database.fetch_one(query=query, values={"uid": uid})