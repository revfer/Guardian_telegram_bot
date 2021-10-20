from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_dost = KeyboardButton('Доступ')
button_prize = KeyboardButton('Расценка')

start_markup = ReplyKeyboardMarkup(resize_keyboard=True)
start_markup.add(button_dost).add(button_prize)
