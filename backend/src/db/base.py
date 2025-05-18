from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from core.config import database_settings


Base = declarative_base()
engine = create_async_engine(url=database_settings.url, plugins=["geoalchemy2"])
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
