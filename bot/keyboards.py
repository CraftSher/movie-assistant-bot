from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button1 = KeyboardButton(text="Поиск по названию")
button2 = KeyboardButton(text="Поиск по части названия")
button3 = KeyboardButton(text="Поиск по дате")
button4 = KeyboardButton(text="Поиск по рейтингу")
button5 = KeyboardButton(text="Поиск по жанру")

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [button1, button2],
        [button3],
        [button4, button5]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)
