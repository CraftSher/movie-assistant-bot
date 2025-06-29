from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from MovieAssistantBot.bot.states import SearchByDateState
from MovieAssistantBot.bot.keyboards import menu_keyboard
from MovieAssistantBot.bot.config import TMDB_API_KEY
from MovieAssistantBot.database.db import save_history
from MovieAssistantBot.bot.states import SearchByRatingState
import aiohttp

def rating_handlers(dp: Dispatcher):
    @dp.message(lambda m: m.text == "Поиск по рейтингу")
    async def ask_rating(message: Message, state: FSMContext):
        await message.answer("Введите минимальный рейтинг (например, 7.5):")
        await state.set_state(SearchByRatingState.waiting_for_rating)

    @dp.message(SearchByRatingState.waiting_for_rating)
    async def process_rating(message: Message, state: FSMContext):
        try:
            rating = float(message.text.strip())
            if not (0 < rating <= 10):
                raise ValueError()
        except ValueError:
            await message.answer("⛔ Введите число от 0 до 10.")
            return

        await state.clear()
        await save_history(message.from_user.id, "rating", str(rating))

        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ru-RU",
            "sort_by": "vote_average.desc",
            "vote_count.gte": 100,
            "vote_average.gte": rating,
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
