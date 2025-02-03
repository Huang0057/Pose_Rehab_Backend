from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.game import GameRecordCreate, GameRecordResponse
from app.crud.game import create_game_record, get_user_game_records,delete_game_record
from app.database import get_db
from app.auth import get_current_user
from app.models.base import User
from typing import List
from datetime import date

router = APIRouter()

@router.post("/add_records", response_model=GameRecordResponse)
async def add_record(
    game_data: GameRecordCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    record = await create_game_record(db, current_user.uid, game_data)
    return record

@router.delete("/delete_record/{record_id}", status_code=204)
async def delete_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    success = await delete_game_record(db, record_id, current_user.uid)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="記錄不存在或無權限刪除"
        )
    return None

@router.get("/records/{part:path}", response_model=List[GameRecordResponse])
async def get_records(
    part: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    records = await get_user_game_records(
        db,
        current_user.uid,
        part if part != "all" else None
    )
    return records