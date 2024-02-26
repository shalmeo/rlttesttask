from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def input_aggregation_period(message: Message):
    print(message)
