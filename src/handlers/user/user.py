import asyncio
import html
from dataclasses import dataclass

from aiogram import Router, F, Bot
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from config import NOTIFICATIONS_CHANNEL_ID, NOTIFICATIONS_THREAD
from src.create_bot import telegram_client
from src.filters.is_admin_filter import IsAdminFilter
from src.utils import logger


ALL_MENTION_KEYWORD = '@all'


@dataclass
class MentionInfo:
    telegram_id: int
    first_name: str
    username: str | None


class CreateNotification(StatesGroup):
    enter_notification_message = State()


async def handle_start_command(message: Message, state: FSMContext):
    await state.clear()
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Создать упоминание')]],
        is_persistent=True, resize_keyboard=True
    )

    await message.answer(
        text=f'Привет, {html.escape(message.from_user.first_name)}!',
        reply_markup=markup
    )


async def create_notification(message: Message, state: FSMContext):
    await state.set_state(CreateNotification.enter_notification_message)
    text = (
        f'Введите сообщение, которое будет отправлено в уведомления. \n\n'
        f'Там, где нужно вставить упоминание пользователей, напишите {ALL_MENTION_KEYWORD}'
    )
    await message.answer(text=text)


async def handle_notification_text(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отправляем уведомление...')

    if ALL_MENTION_KEYWORD not in message.text:
        await message.answer('Вы не ввели ключевое слово для упоминания!')
        return

    try:
        await send_notification(bot=message.bot, text=message.html_text)
    except Exception as e:
        logger.error(e)
        await message.answer('❌ Не получилось отправить уведомление')
    else:
        await message.answer('✅ Уведомление отправлено успешно!')


def split_text(text, max_length: int = 3000):
    result = []
    start = 0

    while start < len(text):
        end = start + max_length
        end = len(text) if end >= len(text) else text.rfind(' ', start, end)

        if end == -1 or end == start:
            result.append(text[start:end + 1])
        else:
            result.append(text[start:end])
        start = end + 1

    return result


async def send_notification(bot: Bot, text: str):
    chat_members = await get_chat_members()

    mention_text = ' '.join(
        f'@{i.username}' if i.username else f'<a href="tg://user?id={i.telegram_id}">{i.first_name}</a>'
        for i in chat_members
    )
    mention_text_parts = split_text(mention_text)

    for part in mention_text_parts:
        text = text.replace(ALL_MENTION_KEYWORD, part)
        await bot.send_message(
            chat_id=NOTIFICATIONS_CHANNEL_ID, message_thread_id=NOTIFICATIONS_THREAD,
            text=text, disable_web_page_preview=True
        )
        await asyncio.sleep(0.2)


async def get_chat_members() -> list[MentionInfo]:
    participants = []

    async with telegram_client as client:
        async for user in client.iter_participants(NOTIFICATIONS_CHANNEL_ID):
            if user.bot:
                continue

            mention_info = MentionInfo(
                telegram_id=user.id, first_name=user.first_name, username=user.username
            )
            participants.append(mention_info)

    return participants


def register_user_handlers(router: Router):
    router.message.filter(IsAdminFilter(), F.chat.type == ChatType.PRIVATE)

    # Команда /start
    router.message.register(handle_start_command, CommandStart())

    # Создание новости
    router.message.register(create_notification, F.text == 'Создать упоминание')

    # Ввод сообщения
    router.message.register(handle_notification_text, CreateNotification.enter_notification_message)
