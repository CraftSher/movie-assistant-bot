from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from MovieAssistantBot.bot.states import SearchByDateState
from MovieAssistantBot.bot.keyboards import menu_keyboard
from MovieAssistantBot.bot.config import TMDB_API_KEY
from MovieAssistantBot.database.db import save_history
from MovieAssistantBot.bot.states import SearchByPartialTitleState
import aiohttp

def partial_title_handlers(dp: Dispatcher):
    @dp.message(lambda m: m.text == "Поиск по части названия")
    async def ask_partial(message: Message, state: FSMContext):
        await message.answer("Введите часть названия фильма:")
        await state.set_state(SearchByPartialTitleState.waiting_for_partial_title)

    @dp.message(SearchByPartialTitleState.waiting_for_partial_title)
    async def process_partial(message: Message, state: FSMContext):
        query = message.text
        await state.clear()
        await save_history(message.from_user.id, "partial_title", query)

        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": query,
            "language": "ru-RU",
            "page": 1
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                results = data.get("results", [])

                if not results:
                    await message.answer("Фильмы не найдены 😕", reply_markup=menu_keyboard)
                    return

                for movie in results[:5]:
                    title = movie.get("title", "Без названия")
                    overview = movie.get("overview", "Описание недоступно")
                    release_date = movie.get("release_date", "Дата не указана")
                    rating = movie.get("vote_average", "—")
                    poster_path = movie.get("poster_path")

                    text = f"<b>{title}</b>\n📅 <i>{release_date}</i>\n⭐ <b>Рейтинг:</b> {rating}\n\n{overview}"
                    if poster_path:
                        photo_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                        await message.answer_photo(photo=photo_url, caption=text[:1024], reply_markup=menu_keyboard)
                    else:
                        await message.answer(text, reply_markup=menu_keyboard)
