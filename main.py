from fastapi import FastAPI
from app.api.endpoints import game, users, checkin
from fastapi.middleware.cors import CORSMiddleware
from app.database import database
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:    
    await database.connect()
    yield    
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
app.include_router(checkin.router, prefix="/api/checkin", tags=["checkin"])
app.include_router(game.router,prefix="/api/game",tags=["game"])
