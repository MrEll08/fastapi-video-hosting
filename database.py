from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from typing import Annotated, ClassVar
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///database/database.db"  # Локальный файл рядом с проектом
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
create_session = async_sessionmaker(bind=engine, expire_on_commit=False, autocommit=False, autoflush=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=datetime.now)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
