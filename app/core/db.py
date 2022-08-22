from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        """Автоматически именуем таблицы в БД по имени класса."""
        return cls.__name__.lower()

    """Во все таблицы добавляем поле с ID."""
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Генерируем асинхронные сессии для работы с БД."""
    async with AsyncSessionLocal() as async_session:
        yield async_session