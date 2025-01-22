from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as user_crud

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def create_user(user: UserCreate):
    """
    註冊新用戶
    """
    # 檢查用戶名是否存在
    existing_user = await user_crud.get_user_by_username(username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # 創建新用戶
    return await user_crud.create_user(user=user)