from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

rates_button = InlineKeyboardButton(
    text='Курс',
    callback_data='rates_button'
)

converter_button = InlineKeyboardButton(
    text='Конвертер',
    callback_data='converter_button'
)

main_kb = InlineKeyboardMarkup(inline_keyboard=[[rates_button, converter_button]])
