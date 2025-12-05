from aiogram.types import Message, User


def get_username(message: Message) -> str | None:
    """Get the username of the user who sent the message.

    Args:
        message (Message): The message from which to extract the username.

    Returns:
        str | None: The username of the user, or None if not available.
    """
    return message.from_user.username


def get_user(message: Message) -> User | None:
    """Get the user who sent the message.

    Args:
        message (Message): The message from which to extract the user.

    Returns:
        User | None: The user who sent the message, or None if not available.
    """
    return message.from_user
