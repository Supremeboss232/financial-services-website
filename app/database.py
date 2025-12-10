# database.py
# Establishes connection to SQL database (Postgres/MySQL) and ORM setup.

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings # Assuming config.py defines DATABASE_URL

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as db:
        yield db
