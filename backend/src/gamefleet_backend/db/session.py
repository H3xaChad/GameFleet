import os
from dotenv import load_dotenv
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


load_dotenv()

# Build DATABASE_URL from individual environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "gamefleet")
DB_USER = os.getenv("DB_USER", "gamefleet")
DB_PASSWORD = os.getenv("DB_PASSWORD", "gamefleet")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Fallback to legacy DATABASE_URL if provided
if legacy_url := os.getenv("DATABASE_URL"):
    DATABASE_URL = legacy_url

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
