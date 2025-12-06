from abc import ABC, abstractmethod

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class BaseConversation(ABC):
    def __init__(self):
        self.router = Router()
        self._register_handlers()

    @abstractmethod
    def _register_handlers(self):
        """Зарегистрировать хендлеры в self.router"""
        pass

    @abstractmethod
    async def start(self, message: Message, state: FSMContext) -> None:
        """Запустить начальный шаг диалога"""
        pass

    @abstractmethod
    async def finish(self, state: FSMContext):
        """Завершить диалог"""
        pass
