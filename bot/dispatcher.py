from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers.commands import commands_router
from bot.handlers.fsm.documents_fsm import documents_fsm_router
from bot.handlers.faq import faq_router


def setup_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(commands_router)
    dp.include_router(documents_fsm_router)
    dp.include_router(faq_router)
    return dp
