from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

URL_DATABASE = "postgresql+asyncpg://postgres:test123@172.18.0.1:5432/feedbackDb"

engine = create_async_engine(URL_DATABASE)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
  pass