from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart)
async def start_command(message: Message):
    await message.answer(text=f'Привет, <b>{message.from_user.first_name}</b>!\nЧем я могу помочь?')


@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(
        text=f'Кнопка "<b>Курс</b>" предоставит Вам актуальный перечень '
             f'курсов всех валют, выраженных в российских рублях.\n\n'
             f'"<b>Конвертер</b>" позволяет преобразовать заданное количество денежных единиц из одной валюты в другую'
    )
