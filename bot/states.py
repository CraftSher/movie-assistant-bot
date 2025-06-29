from aiogram.fsm.state import State, StatesGroup

class SearchByTitleState(StatesGroup):
    waiting_for_title = State()

class SearchByPartialTitleState(StatesGroup):
    waiting_for_partial_title = State()

class SearchByDateState(StatesGroup):
    waiting_for_year = State()

class SearchByRatingState(StatesGroup):
    waiting_for_rating = State()

class SearchByGenreState(StatesGroup):
    waiting_for_genre = State()
