from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup, default_state

from keyboards.main_kb import main_kb


class FSMCurrencyConverter(StatesGroup):
    first_currency = State()   # Состояние ожидания выбора конвертируемой валюты
    second_currency = State()  # Состояние ожидания выбора валюты, в которую необходимо конвертировать
    quantity = State()         # Состояние ожидания ввода количества конвертируемой валюты


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    await message.answer(
        text=f'Привет, <b>{message.from_user.first_name}</b>!\nЧем я могу помочь?',
        reply_markup=main_kb
    )


@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(
        text=f'Кнопка <b>Курс</b> предоставит Вам актуальный перечень '
             f'курсов всех валют, выраженных в российских рублях.\n\n'
             f'<b>Конвертер</b> позволяет преобразовать заданное количество денежных единиц из одной валюты в другую'
    )
