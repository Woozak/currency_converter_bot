from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from currencies import currencies

currencies_kb_builder = InlineKeyboardBuilder()
buttons = []

for code, name in currencies.items():
    buttons.append(
        InlineKeyboardButton(text=f'{name[0]} {name[1]}', callback_data=code)
    )

currencies_kb_builder.row(*buttons, width=2)

currencies_kb = currencies_kb_builder.as_markup()
