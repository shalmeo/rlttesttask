import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from motor.motor_asyncio import AsyncIOMotorClient

from rlttest.bot import handlers


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(process)-7s %(module)-20s %(message)s",
    )

    bot = Bot(os.getenv("BOT_TOKEN"))
    storage = MemoryStorage()
    dispatcher = Dispatcher()

    mongo_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))

    handlers.setup(dispatcher)

    try:
        await mongo_client.admin.command("ping")
        await dispatcher.start_polling(bot)
    finally:
        await storage.close()
        await bot.session.close()
        mongo_client.close()


if __name__ == "__main__":
    asyncio.run(main())
