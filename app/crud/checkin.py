from sqlalchemy import extract, select
from app.models.base import UserCheckin
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

async def get_monthly_checkins(db: AsyncSession, user_uid: str, year: int, month: int):
    # 使用 select 語句替代 query
    query = select(UserCheckin).where(
        UserCheckin.user_uid == user_uid,
        extract('year', UserCheckin.checkin_date) == year,
        extract('month', UserCheckin.checkin_date) == month
    )
    result = await db.execute(query)
    return result.scalars().all()

async def create_checkin(db: AsyncSession, user_uid: str, checkin_date: date):    
    # 檢查是否存在
    query = select(UserCheckin).where(
        UserCheckin.user_uid == user_uid,
        UserCheckin.checkin_date == checkin_date
    )
    result = await db.execute(query)
    existing_record = result.scalar_one_or_none()
    
    if existing_record:
        if existing_record.signed_in:
            return existing_record
        existing_record.signed_in = True
        await db.commit()
        return existing_record    
    
    # 建立新記錄
    new_checkin = UserCheckin(
        user_uid=user_uid,
        checkin_date=checkin_date,
        signed_in=True
    )
    db.add(new_checkin)
    await db.commit()
    await db.refresh(new_checkin)
    return new_checkin