import asyncio

from aiogram import Bot, Dispatcher

from config.config import Config, load_config
from handlers import handlers
from keyboards.menu_kb import main_menu


async def main():
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(handlers.router)

    await bot.set_my_commands(main_menu)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
