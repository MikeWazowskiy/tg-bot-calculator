from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.misc import TgKeys
from bot.handlers import register_all_handlers
from bot.database import db

import logging

async def __on_start_up(dp: Dispatcher) -> None:
    database = db()

    logging.basicConfig(level=logging.INFO)
    register_all_handlers(dp, database)


def start_bot():
    bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)