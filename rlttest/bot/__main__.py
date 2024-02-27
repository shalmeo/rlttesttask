import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from motor.motor_asyncio import AsyncIOMotorClient

from rlttest.bot import handlers
from rlttest.core.usecases.get_salaries import AggregateSalaries
from rlttest.infrastructure.database.gateway.salary import SalaryGateway


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(process)-7s %(module)-20s %(message)s",
    )

    bot = Bot(os.getenv("BOT_TOKEN"))
    dispatcher = Dispatcher()

    mongo_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    database = mongo_client.get_database(os.getenv("DB_NAME"))

    handlers.setup(dispatcher)

    try:
        await dispatcher.start_polling(
            bot,
            aggragate_salaries=AggregateSalaries(
                salary_gateway=SalaryGateway(database)
            ),
        )
    finally:
        await bot.session.close()
        mongo_client.close()


if __name__ == "__main__":
    asyncio.run(main())
