import os
from typing import Final
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

BOT_TOKEN: Final[str] = os.getenv('BOT_TOKEN', 'define me')
OWNER_IDS: Final[tuple] = tuple(int(i) for i in str(os.getenv('BOT_OWNER_IDS')).split(','))

# Информация о клиенте телеграм
CLIENT_NAME: Final[str] = os.getenv('CLIENT_NAME')
CLIENT_API_ID: Final[int] = int(os.getenv('CLIENT_API_ID'))
CLIENT_API_HASH: Final[str] = os.getenv('CLIENT_API_HASH')

# Информация о канале, в который постить уведомления
NOTIFICATIONS_CHANNEL_ID: Final[int] = int(os.getenv('NOTIFICATIONS_CHANNEL_ID'))
NOTIFICATIONS_THREAD: Final[int | None] = int(os.getenv('NOTIFICATIONS_THREAD'))
