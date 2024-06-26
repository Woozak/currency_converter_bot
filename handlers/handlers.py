from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

from keyboards.main_kb import main_kb
from keyboards.currencies_kb import currencies_kb
from currency_functions import get_exchange_rates, currency_converter, is_number
from currencies import currencies


class FSMCurrencyConverter(StatesGroup):
    first_currency = State()  # Состояние ожидания выбора конвертируемой валюты
    second_currency = State()  # Состояние ожидания выбора валюты, в которую необходимо конвертировать
    quantity = State()  # Состояние ожидания ввода количества конвертируемой валюты


router = Router()


@router.message(Command(commands=['start', 'cancel']))
async def start_and_cancel_commands(message: Message, state: FSMContext):
    await message.answer(
        text=f'Привет, <b>{message.from_user.first_name}</b>!\nЧем я могу помочь?',
        reply_markup=main_kb
    )
    await state.set_state(default_state)


@router.message(Command(commands='help'))
async def help_command(message: Message, state: FSMContext):
    await message.answer(
        text=f'Кнопка <b>Курс</b> предоставит Вам актуальный перечень '
             f'курсов всех валют, выраженных в российских рублях.\n\n'
             f'<b>Конвертер</b> позволяет преобразовать заданное количество денежных единиц из одной валюты в другую',
        reply_markup=main_kb
    )
    await state.set_state(default_state)


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

    await callback.message.answer(text='Введите количество')

    await state.set_state(FSMCurrencyConverter.quantity)
    await callback.answer()


@router.message(is_number, StateFilter(FSMCurrencyConverter.quantity))
async def enter_quantity(message: Message, state: FSMContext):
    await state.update_data(quantity=float(message.text.replace(',', '.')))

    data = await state.get_data()

    await message.answer(text=currency_converter(
            first=data['first_currency'],
            second=data['second_currency'],
            quantity=data['quantity']
        ),
        reply_markup=main_kb
    )
    await state.set_state(default_state)


@router.message(StateFilter(FSMCurrencyConverter.quantity))
async def enter_incorrect_quantity(message: Message):
    await message.answer(text='Пожалуйста, введите число')


@router.message(~StateFilter(FSMCurrencyConverter.quantity))
async def other_message(message: Message):
    await message.answer(text='Пожалуйста, воспользуйтесь кнопками')
