from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.base import GameRecord,User
from datetime import date
from app.schemas.game import GameRecordCreate

async def create_game_record(
    db: AsyncSession,
    user_uid: str,
    game_data: GameRecordCreate
):
    # 建立新的遊戲記錄
    new_record = GameRecord(
        user_uid=user_uid,
        **game_data.model_dump()
    )
    db.add(new_record)
    
    # 更新用戶的 coins
    query = select(User).where(User.uid == user_uid)
    result = await db.execute(query)
    user = result.scalar_one()
    user.coins += game_data.coins_earned
    
    # 一次性提交所有更改
    await db.commit()
    await db.refresh(new_record)
    return new_record

async def delete_game_record(
    db: AsyncSession,
    record_id: int,
    user_uid: str
) -> bool:
    """刪除遊戲記錄並扣除對應的 coins"""
    # 先查詢記錄
    query = select(GameRecord).where(
        GameRecord.id == record_id,
        GameRecord.user_uid == user_uid
    )
    result = await db.execute(query)
    record = result.scalar_one_or_none()
    
    if not record:
        return False
    
    # 查詢並更新用戶的 coins
    user_query = select(User).where(User.uid == user_uid)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one()
    
    # 確保扣除後不會變成負數
    if user.coins >= record.coins_earned:
        user.coins -= record.coins_earned
    else:
        user.coins = 0
        
    # 刪除記錄
    await db.delete(record)
    
    # 一次性提交所有更改
    await db.commit()
    return True

async def get_user_game_records(
    db: AsyncSession,
    user_uid: str,
    part: str | None = None
):
    query = select(GameRecord).where(
        GameRecord.user_uid == user_uid
    )
    
    if part:
        query = query.where(GameRecord.part == part)
        
    query = query.order_by(GameRecord.play_date.desc(), GameRecord.start_time.desc())
    
    result = await db.execute(query)
    return result.scalars().all()