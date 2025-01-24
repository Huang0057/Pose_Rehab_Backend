from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import databases
from typing import AsyncGenerator
from app.config import settings

DATABASE_URL = settings.DATABASE_URL
DATABASE_URL_ASYNC = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
async_engine = create_async_engine(DATABASE_URL_ASYNC)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
   async with async_session() as session:
       try:
           yield session
           await session.commit()
       except Exception as e:
           await session.rollback()
           raise e
       finally:
           await session.close()