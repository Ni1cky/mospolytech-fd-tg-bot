from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from config import config


class Database:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session: async_sessionmaker[AsyncSession] | None = None

    async def connect(self) -> None:
        db = config.database
        self.engine = create_async_engine(db.url)
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def disconnect(self) -> None:
        await self.engine.dispose()


database = Database()


def setup_database(dp: Dispatcher):
    dp.startup.register(database.connect)
    dp.shutdown.register(database.disconnect)