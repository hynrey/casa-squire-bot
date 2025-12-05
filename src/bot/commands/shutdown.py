from aiogram.types import Message
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext

from src.bot.commands.base import BaseCommand


class ShutdownCommand(BaseCommand):
    async def execute(self, message: Message, command: CommandObject, state: FSMContext) -> None:
        await self.conversation.start(message, state)
