from aiogram import Dispatcher, Router

from .user import register_user_handlers
from .errors import register_errors_handler


def register_all_handlers(dp: Dispatcher):
    user_router = Router(name='user_router')
    register_user_handlers(router=user_router)
    register_errors_handler(router=user_router)

    dp.include_router(user_router)
