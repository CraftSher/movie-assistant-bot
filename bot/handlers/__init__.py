from .search_by_title import title_handlers
from .search_by_partial_title import partial_title_handlers
from .search_by_date import date_handlers
from .search_by_rating import rating_handlers
from .search_by_genre import genre_handlers
from .history import router as history_router


def register_handlers(dp):
    title_handlers(dp)
    partial_title_handlers(dp)
    date_handlers(dp)
    rating_handlers(dp)
    genre_handlers(dp)
    dp.include_router(history_router)
