from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import MetaData
from alembic import command
from alembic.config import Config

from config import config


class Database:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session: async_sessionmaker[AsyncSession] | None = None
        self.metadata = MetaData()

    async def connect(self) -> None:
        """Подключение к базе данных."""
        db = config.database
        self.engine = create_async_engine(db.url, echo=True)  # echo=True для отладки
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def disconnect(self) -> None:
        """Отключение от базы данных."""
        if self.engine:
            await self.engine.dispose()

    async def create_tables(self) -> None:
        """Создание таблиц в базе данных."""
        from database.sqlalchemy_base import Base
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except SQLAlchemyError as e:
            print(f"Error creating tables: {e}")

    async def drop_tables(self) -> None:
        """Удаление всех таблиц из базы данных."""
        from database.sqlalchemy_base import Base
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
        except SQLAlchemyError as e:
            print(f"Error dropping tables: {e}")


database = Database()


def setup_database(dp: Dispatcher):
    """
    Регистрация событий старта и завершения работы с базой данных
    в контексте Telegram-бота.
    """
    dp.startup.register(database.connect)
    dp.shutdown.register(database.disconnect)


def run_migrations():
    """
    Запуск миграций с использованием Alembic.
    """
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("Migrations applied successfully.")
    except Exception as e:
        print(f"Error during migrations: {e}")


async def get_session() -> AsyncSession:
    """
    Утилита для получения сессии базы данных.
    """
    if not database.session:
        raise RuntimeError("Database is not connected. Call 'database.connect()' first.")
    return database.session()
