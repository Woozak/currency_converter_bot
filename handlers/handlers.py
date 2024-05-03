from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

from keyboards.main_kb import main_kb
from keyboards.currencies_kb import currencies_kb
from currency_functions import get_exchange_rates
from currencies import currencies


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


@router.message(Command(commands='help'), StateFilter(default_state))
async def help_command(message: Message):
    await message.answer(
        text=f'Кнопка <b>Курс</b> предоставит Вам актуальный перечень '
             f'курсов всех валют, выраженных в российских рублях.\n\n'
             f'<b>Конвертер</b> позволяет преобразовать заданное количество денежных единиц из одной валюты в другую',
        reply_markup=main_kb
    )


@router.callback_query(F.data == 'rates_button')
async def rates_button_press(callback: CallbackQuery):
    message_text = get_exchange_rates()

    if message_text != callback.message.text:
        await callback.message.edit_text(
            text=message_text,
            reply_markup=main_kb
        )

    await callback.answer()


@router.callback_query(F.data == 'converter_button')
async def converter_button_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Выберите валюту, которую нужно конвертировать',
        reply_markup=currencies_kb
    )
    await state.set_state(FSMCurrencyConverter.first_currency)


@router.callback_query(F.data.in_(currencies), StateFilter(FSMCurrencyConverter.first_currency))
async def select_first_currency(callback: CallbackQuery, state: FSMContext):
    await state.update_data(first_currency=callback.data)

    await callback.message.edit_text(
        text='Выберите валюту, в которую нужно конвертировать первую выбранную валюту',
        reply_markup=currencies_kb
    )
    await state.set_state(FSMCurrencyConverter.second_currency)


@router.callback_query(F.data.in_(currencies), StateFilter(FSMCurrencyConverter.second_currency))
async def select_second_currency(callback: CallbackQuery, state: FSMContext):
    await state.update_data(second_currency=callback.data)

    await callback.message.edit_text(
        text='Введите количество',
        reply_markup=currencies_kb
    )
    await state.set_state(FSMCurrencyConverter.quantity)
