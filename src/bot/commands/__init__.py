from aiogram import Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.commands.shutdown import ShutdownCommand
from src.bot.commands.start import StartCommand
from src.bot.conversation.shutdown import ShutdownConversation


def command_handler(command_instance):
    async def handler(message: Message, command: CommandObject, state: FSMContext) -> None:
        await command_instance.execute(message, command, state)

    return handler


def register_commands(dp: Dispatcher) -> None:
    dp.message.register(command_handler(StartCommand()), Command("start"))

    shutdown_conversation = ShutdownConversation()

    dp.message.register(
        command_handler(ShutdownCommand(conversation=shutdown_conversation)), Command("shutdown")
    )
    dp.include_router(shutdown_conversation.router)
