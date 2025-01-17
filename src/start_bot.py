from src import bot, dp
from src.handlers import register_all_handlers
from src.utils import logger


async def on_startup():
    # Регистрация хэндлеров
    register_all_handlers(dp)

    logger.info('Бот запущен!')


async def on_shutdown():
    logger.info('Бот остановлен')


async def start_bot():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        # Запускаем поллинг
        await dp.start_polling(bot, close_bot_session=True)
    except Exception as e:
        logger.exception(e)

