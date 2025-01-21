from sqlalchemy.orm import Session
from app.models.base import User
from app.schemas.user import UserCreate
import secrets
import string

def generate_uid(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_user(db: Session, user: UserCreate):
    uid = generate_uid()
    db_user = User(
        username=user.username,
        password=user.password,  # 注意：實際應用中應該對密碼進行雜湊處理
        uid=uid
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()