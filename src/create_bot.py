from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from telethon import TelegramClient

from config import BOT_TOKEN, CLIENT_NAME, CLIENT_API_ID, CLIENT_API_HASH


bot = Bot(token=BOT_TOKEN, disable_web_page_preview=True, parse_mode='HTML')
telegram_client = TelegramClient(CLIENT_NAME, CLIENT_API_ID, CLIENT_API_HASH, device_model="Telegram Desktop", system_version="Windows 10")

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
