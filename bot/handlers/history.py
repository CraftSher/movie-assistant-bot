from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from MovieAssistantBot.database.db import get_history

router = Router()

@router.message(Command("history"))
async def show_history(message: Message):
    history_entries = await get_history(message.from_user.id)

    if not history_entries:
        await message.answer("🕵️ У вас пока нет истории поиска.")
        return

    text = "📜 Ваша история поиска:\n"
    for i, entry in enumerate(history_entries, 1):
        text += f"{i}. 🔎 Тип: {entry.search_type.capitalize()} | Запрос: {entry.query}\n"

    await message.answer(text)
