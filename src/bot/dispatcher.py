from aiogram import Dispatcher

from src.bot.commands import register_commands


def register_callbacks(dp: Dispatcher) -> None:
    register_commands(dp=dp)
