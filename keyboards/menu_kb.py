from aiogram.types import BotCommand

main_menu = [
    BotCommand(command='/start',
               description='Запустить бота'),
    BotCommand(command='/help',
               description='Справка по работе бота'),
    BotCommand(command='/cancel',
               description='Отменить текущую операцию')
]
