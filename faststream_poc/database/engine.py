from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from faststream_poc.settings import settings

from .models import Base

engine = create_async_engine(url=settings.database_url)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_session():
    async with async_session() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
