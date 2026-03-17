from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from config import get_settings

settings = get_settings()

def _engine():
    kw = {"echo": not settings.is_production, "pool_pre_ping": True}
    if settings.is_postgres: kw.update({"pool_size": 5, "max_overflow": 10})
    elif settings.is_sqlite: kw["connect_args"] = {"check_same_thread": False}
    return create_async_engine(settings.database_url, **kw)

engine = _engine()
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase): pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as s:
        try:
            yield s
            await s.commit()
        except Exception:
            await s.rollback()
            raise

async def init_db():
    if settings.is_sqlite:
        async with engine.begin() as c:
            await c.run_sync(Base.metadata.create_all)
