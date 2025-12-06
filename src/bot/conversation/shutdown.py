import asyncio
from enum import Enum

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.conversation.base import BaseConversation
from src.bot.states.shutdown import ShutdownState
from src.utils.shutdown import abort_shutdown, schedule_shutdown


class ShutdownAction(Enum):
    NOW = 0
    H1 = 3600
    H2 = 7200
    H3 = 10800
    H4 = 14400
    ABORT = -1

    @classmethod
    def from_callback(cls, raw: str) -> "ShutdownAction":
        if raw == "now":
            return cls.NOW
        if raw == "abort":
            return cls.ABORT
        if raw.isdigit():
            return cls(int(raw))
        raise ValueError(f"Unknown shutdown action: {raw!r}")

    @property
    def callback_value(self) -> str:
        if self is ShutdownAction.NOW:
            return "now"
        if self is ShutdownAction.ABORT:
            return "abort"
        return str(int(self.value))


class ShutdownConfirmAction(str, Enum):
    YES = "yes"
    NO = "no"

    @classmethod
    def from_callback(cls, raw: str) -> "ShutdownConfirmAction":
        try:
            return cls(raw)
        except ValueError:
            raise ValueError(f"Unknown confirm action: {raw!r}") from None


class ShutdownConversation(BaseConversation):

    def _register_handlers(self):
        """Register handlers for the link conversation."""
        self.router.callback_query.register(
            self.ask_time, ShutdownState.ask_time, F.data.startswith("shutdown:")
        )
        self.router.callback_query.register(
            self.ask_now_confirm, ShutdownState.ask_now_confirm, F.data.startswith("now_confirm:")
        )

    def __build_time_keyboard(self, has_pending: bool) -> InlineKeyboardMarkup:
        """
        Плитка:
        Сейчас, 1ч, 2ч, 3ч, 4ч, (Опционально) Отменить выключение
        """
        builder = InlineKeyboardBuilder()

        builder.button(
            text="⚡ Сейчас", callback_data=f"shutdown:{ShutdownAction.NOW.callback_value}"
        )
        builder.button(
            text="⏰ Через 1 час", callback_data=f"shutdown:{ShutdownAction.H1.callback_value}"
        )
        builder.button(
            text="⏰ Через 2 часа", callback_data=f"shutdown:{ShutdownAction.H2.callback_value}"
        )
        builder.button(
            text="⏰ Через 3 часа", callback_data=f"shutdown:{ShutdownAction.H3.callback_value}"
        )
        builder.button(
            text="⏰ Через 4 часа", callback_data=f"shutdown:{ShutdownAction.H4.callback_value}"
        )

        builder.adjust(1, 2, 2)

        if has_pending:
            builder.button(
                text="❌ Отменить выключение",
                callback_data=f"shutdown:{ShutdownAction.ABORT.callback_value}",
            )
            builder.adjust(1, 2, 2, 1)

        return builder.as_markup()

    def __build_confirm_keyboard(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text="✅ Да", callback_data="now_confirm:yes")
        builder.button(text="✖️ Нет", callback_data="now_confirm:no")
        return builder.as_markup()

    @staticmethod
    def __format_delay_text(seconds: int) -> str:
        if seconds == 0:
            return "💤 Компьютер начнёт выключаться прямо сейчас!"
        if seconds < 60:
            return f"⏱️ Компьютер выключится через {seconds} секунд"
        if seconds % 3600 == 0:
            hours = seconds // 3600
            if hours == 1:
                return "⏳ Компьютер выключится через 1 час"
            if 2 <= hours <= 4:
                return f"⏳ Компьютер выключится через {hours} часа"
            return f"⏳ Компьютер выключится через {hours} часов"
        else:
            mins = seconds // 60
            return f"⏳ Компьютер выключится примерно через {mins} минут"

    @staticmethod
    async def _reset_state(state: FSMContext) -> None:
        """Сброс shutdown-состояния."""
        await state.update_data(pending=False, delay_seconds=None)
        await state.clear()

    async def _notify_before_shutdown(
        self, callback: CallbackQuery, state: FSMContext, seconds: int
    ):
        if seconds <= 0:
            await self._reset_state(state)
            return
        if seconds > 300:
            await asyncio.sleep(seconds - 300)
            await callback.bot.send_message(
                chat_id=callback.from_user.id, text="⚠️ Компьютер выключится через 5 минут!"
            )

        await asyncio.sleep(min(300, seconds))
        await callback.bot.send_message(
            chat_id=callback.from_user.id, text="💤 Компьютер выключается прямо сейчас!"
        )
        await self._reset_state(state)

    async def start(self, message: Message, state: FSMContext):
        data = await state.get_data()
        has_pending = data.get("pending", False)

        keyboard = self.__build_time_keyboard(has_pending)
        await message.answer(text="🖥️ Когда выключить компьютер?", reply_markup=keyboard)
        await state.set_state(ShutdownState.ask_time)

    async def ask_time(self, callback: CallbackQuery, state: FSMContext):
        chat_id = callback.message.chat.id
        raw_action = callback.data.split(":")[1]
        action = ShutdownAction.from_callback(raw_action)

        await callback.message.delete()

        if action is ShutdownAction.ABORT:
            abort_shutdown()
            await self._reset_state(state)
            await callback.bot.send_message(
                chat_id=chat_id, text="❌ Запланированное выключение отменено."
            )
            return

        if action is ShutdownAction.NOW:
            keyboard = self.__build_confirm_keyboard()
            await state.set_state(ShutdownState.ask_now_confirm)
            await callback.bot.send_message(
                chat_id=chat_id,
                text="⚠️ Ты точно хочешь выключить компьютер прямо сейчас?",
                reply_markup=keyboard,
            )
            return

        seconds: int = action.value
        delay_text = self.__format_delay_text(seconds)

        schedule_shutdown(seconds)

        await callback.bot.send_message(chat_id=chat_id, text=delay_text)
        await state.update_data(
            delay_seconds=seconds,
            pending=True,
        )

        asyncio.create_task(
            self._notify_before_shutdown(
                callback=callback,
                state=state,
                seconds=seconds,
            )
        )

    async def ask_now_confirm(self, callback: CallbackQuery, state: FSMContext):
        chat_id = callback.message.chat.id
        raw = (callback.data or "").split(":", 1)[1]
        action = ShutdownConfirmAction.from_callback(raw)

        await callback.message.delete()

        if action == ShutdownConfirmAction.YES:
            seconds = 0
            delay_text = self.__format_delay_text(seconds)
            await callback.bot.send_message(chat_id=chat_id, text=delay_text)
            schedule_shutdown(seconds)
            await self._reset_state(state)
            return

        await callback.bot.send_message(
            chat_id=chat_id, text="👌 Хорошо не буду выключать компьютер"
        )
        await self._reset_state(state)

    async def finish(self, state: FSMContext):
        return await super().finish(state)
