from aiogram import Dispatcher

from rlttest.bot.handlers import salaries


def setup(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(salaries.router)
