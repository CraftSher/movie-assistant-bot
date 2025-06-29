from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from MovieAssistantBot.bot.states import SearchByDateState
from MovieAssistantBot.bot.keyboards import menu_keyboard
from MovieAssistantBot.bot.config import TMDB_API_KEY
from MovieAssistantBot.database.db import save_history
import aiohttp

def date_handlers(dp: Dispatcher):
    @dp.message(lambda m: m.text == "Поиск по дате")
    async def ask_year(message: Message, state: FSMContext):
        await message.answer("Введите год выхода фильма (например, 1999):")
        await state.set_state(SearchByDateState.waiting_for_year)

    @dp.message(SearchByDateState.waiting_for_year)
    async def process_year(message: Message, state: FSMContext):
        year = message.text.strip()
        if not (year.isdigit() and len(year) == 4):
            await message.answer("⛔ Введите корректный год из 4 цифр.")
            return

        await state.clear()
        await save_history(message.from_user.id, "year", year)

        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ru-RU",
            "sort_by": "popularity.desc",
            "primary_release_year": year,
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
