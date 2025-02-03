from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.models.base import User, UserCheckin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(db: AsyncSession, username: str, password: str):
    hashed_password = pwd_context.hash(password)
    new_user = User(
        username=username,
        password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def verify_password(plain_password: str, hashed_password: str):
    """驗證密碼"""
    return pwd_context.verify(plain_password, hashed_password)

async def verify_user(db: AsyncSession, username: str, password: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
        
    if not pwd_context.verify(password, user.password):
        return None
        
    return user

async def get_streak_days(db: AsyncSession, uid: str):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    # 取得昨天的打卡記錄
    yesterday_query = select(UserCheckin).where(
        UserCheckin.user_uid == uid,
        UserCheckin.checkin_date == yesterday,
        UserCheckin.signed_in == True
    )
    yesterday_result = await db.execute(yesterday_query)
    yesterday_checkin = yesterday_result.scalar_one_or_none()
    
    if not yesterday_checkin:
        return 1
    
    # 查詢連續打卡天數
    streak_count = 1
    current_date = yesterday
    
    while True:
        previous_date = current_date - timedelta(days=1)
        previous_query = select(UserCheckin).where(
            UserCheckin.user_uid == uid,
            UserCheckin.checkin_date == previous_date,
            UserCheckin.signed_in == True
        )
        previous_result = await db.execute(previous_query)
        previous_checkin = previous_result.scalar_one_or_none()
        
        if not previous_checkin:
            break
            
        streak_count += 1
        current_date = previous_date
    
    return streak_count + 1

async def get_user_by_id(db: AsyncSession, uid: str):
    query = select(User).where(User.uid == uid)
    result = await db.execute(query)
    return result.scalar_one_or_none()