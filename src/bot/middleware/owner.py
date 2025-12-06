import logging
from typing import Any, Awaitable, Callable, Set

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, User


class OwnerMiddleware(BaseMiddleware):
    def __init__(self, owner_ids: Set[int]):
        self.owner_ids = set(owner_ids)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        chat: Chat | None = data.get("event_chat")

        if not chat.type == "private":
            logging.info("Chat is not private")
            return

        if user is None:
            logging.info("User is None")
            return

        if user.id not in self.owner_ids:
            logging.info(f"User {user.id} is not owner")
            return

        return await handler(event, data)
