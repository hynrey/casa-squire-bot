from abc import ABC, abstractmethod

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.conversation.base import BaseConversation


class BaseCommand(ABC):

    def __init__(self, conversation: BaseConversation | None = None):
        self.conversation = conversation

    @abstractmethod
    async def execute(self, message: Message, state: FSMContext) -> None:
        pass
