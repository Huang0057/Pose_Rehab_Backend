from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models.base import Base
from app.api.endpoints import users

app = FastAPI()

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 創建資料表
Base.metadata.create_all(bind=engine)

# 根路由
@app.get("/")
def read_root():
    return {"message": "Welcome to Pose Rehab API"}

# 加入路由
app.include_router(users.router, prefix="/users", tags=["users"])