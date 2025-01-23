from fastapi import APIRouter, HTTPException
from app.schemas.user import UserLogin, UserRegister, UserResponse
from app.crud.user import verify_user, create_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserRegister):
    user = await create_user(user_data.username, user_data.password)
    return UserResponse(
        username=user.username,
        uid=user.uid,
        coins=user.coins
    )

@router.post("/login", response_model=UserResponse) 
async def login_user(user_data: UserLogin):
    user = await verify_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="帳號或密碼錯誤"
        )
    return UserResponse(
        username=user.username,
        uid=user.uid,
        coins=user.coins
    )