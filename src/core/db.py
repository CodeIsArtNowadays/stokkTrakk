from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import settings


engine = create_async_engine(
    settings.async_db_url,
    echo=True,
    connect_args={"statement_cache_size": 0},
    pool_size=10,
    max_overflow=10,
    pool_recycle=1800,
)

local_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with local_session.begin() as session:
        yield session


Base = declarative_base()
