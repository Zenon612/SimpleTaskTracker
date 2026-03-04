from typing import Any, AsyncGenerator
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env or environment variable!")

engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[Any, Any]:
    """
    Позволяет использовать Depends для управления сессией БД
    :return: AsyncGenerator
    """
    async with new_session() as session:
        yield session