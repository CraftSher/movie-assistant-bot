from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram import F
from dotenv import load_dotenv
import asyncio
import os
import logging
from MovieAssistantBot.database.db import init_db
from MovieAssistantBot.bot.handlers import register_handlers
from MovieAssistantBot.bot.keyboards import menu_keyboard

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Привет! Я бот для поиска фильмов. Выберите опцию:", reply_markup=menu_keyboard)


def setup():
    init_db()
    register_handlers(dp)


async def main():
    setup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
