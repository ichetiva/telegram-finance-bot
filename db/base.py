from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from credentials import DATABASE_CREDENTIALS

engine = create_async_engine(
    "postgresql+asyncpg://{user}:{password}@{host}/{database}".format(
        **DATABASE_CREDENTIALS
    ), echo=True, future=True
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
