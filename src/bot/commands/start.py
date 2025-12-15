from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.commands.base import AVAILABLE_COMMANDS, BaseCommand


class StartCommand(BaseCommand):
    async def execute(self, message: Message, command: CommandObject, state: FSMContext) -> None:
        await message.answer(f"Привет! Я агент Casa Squire, я помогу тебе управлять твоим домом.\nДоступные команды:\n{"\n".join(AVAILABLE_COMMANDS)}")
