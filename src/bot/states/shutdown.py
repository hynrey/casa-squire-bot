from aiogram.fsm.state import State

from src.bot.states.base import BaseState


class ShutdownState(BaseState):
    """
    State for handling link-related operations.
    """

    ask_time = State()
    ask_now_confirm = State()
