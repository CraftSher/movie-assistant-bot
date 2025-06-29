from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from MovieAssistantBot.bot.states import SearchByDateState
from MovieAssistantBot.bot.keyboards import menu_keyboard
from MovieAssistantBot.bot.config import TMDB_API_KEY
from MovieAssistantBot.database.db import save_history
from MovieAssistantBot.bot.states import SearchByGenreState
import aiohttp

GENRE_MAP = {
    "боевик": 28,
    "приключения": 12,
    "мультфильм": 16,
    "комедия": 35,
    "криминал": 80,
    "документальный": 99,
    "драма": 18,
    "семейный": 10751,
    "фэнтези": 14,
    "история": 36,
    "ужасы": 27,
    "музыка": 10402,
    "детектив": 9648,
    "мелодрама": 10749,
    "фантастика": 878,
    "телевизионный фильм": 10770,
    "триллер": 53,
    "военный": 10752,
    "вестерн": 37
}

def genre_handlers(dp: Dispatcher):
    @dp.message(lambda m: m.text == "Поиск по жанру")
    async def ask_genre(message: Message, state: FSMContext):
        await message.answer("Введите жанр из списка:\n" + ", ".join(GENRE_MAP.keys()))
        await state.set_state(SearchByGenreState.waiting_for_genre)

    @dp.message(SearchByGenreState.waiting_for_genre)
    async def process_genre(message: Message, state: FSMContext):
        genre_name = message.text.strip().lower()
        genre_id = GENRE_MAP.get(genre_name)

        if not genre_id:
            await message.answer("⛔ Жанр не распознан. Используйте из списка:\n" + ", ".join(GENRE_MAP.keys()))
            return

        await state.clear()
        await save_history(message.from_user.id, "genre", genre_name)

        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ru-RU",
            "sort_by": "popularity.desc",
            "with_genres": genre_id,
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
