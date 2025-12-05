import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.settings.logs_settings import LogManager
from src.settings import telegram_settings
from src.bot.dispatcher import register_callbacks
from src.bot.middleware.owner import OwnerMiddleware

bot = Bot(
    token=telegram_settings.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def main():

    logger = logging.getLogger()
    logger.addHandler(LogManager.log_handler())

    logging.info("Registering commands")
    dp = Dispatcher()
    dp.update.middleware(OwnerMiddleware(telegram_settings.owner_ids))

    register_callbacks(dp=dp)
    logging.info("Starting bot")

    await dp.start_polling(bot)
