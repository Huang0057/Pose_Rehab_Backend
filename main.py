from fastapi import FastAPI
from app.api.endpoints import users
from fastapi.middleware.cors import CORSMiddleware
from app.database import database
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # 啟動時連接資料庫
    await database.connect()
    yield
    # 關閉時斷開資料庫連接
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(users.router, prefix="/api/users", tags=["users"])