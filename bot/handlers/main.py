from aiogram import Dispatcher

from bot.handlers.admin import register_admin_handlers
from bot.handlers.user import register_user_handlers


def register_all_handlers(dp: Dispatcher, db) -> None:
    handlers = (
        register_user_handlers,
        register_admin_handlers,
    )
    for handler in handlers:
        handler(dp, db)