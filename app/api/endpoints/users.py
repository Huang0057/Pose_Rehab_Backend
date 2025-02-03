from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserLogin, UserRegister, UserResponse
from app.crud.user import verify_user, create_user, get_streak_days
from app.auth import get_current_user
from app.models.base import User
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    user = await create_user(db, user_data.username, user_data.password)
    return UserResponse(
        username=user.username,
        uid=user.uid,
        coins=user.coins
    )

@router.post("/login", response_model=UserResponse) 
async def login_user(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    user = await verify_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="帳號或密碼錯誤"
        )
    token_data = {
        "sub": user.uid,
        "exp": datetime.now(timezone.utc) + timedelta(days=1)  # token 有效期 1 天
    }
    token = jwt.encode(
        token_data, 
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    streak_days = await get_streak_days(db, user.uid)

    return UserResponse(
        username=user.username,
        uid=user.uid,
        coins=user.coins,
        streak_days=streak_days,
        token=token 
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    streak_days = await get_streak_days(db, current_user.uid)
    return UserResponse(
        username=current_user.username,
        uid=current_user.uid,
        coins=current_user.coins,
        streak_days=streak_days
    )