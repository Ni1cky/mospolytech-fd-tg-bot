import asyncio

from bot.bot import setup_bot
from bot.dispatcher import setup_dispatcher


async def main() -> None:
    dp = setup_dispatcher()
    bot = await setup_bot()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
