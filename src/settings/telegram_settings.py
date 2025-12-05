from typing import Set

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class TelegramSettings(BaseSettings):
    """
    Settings for the Telegram bot.
    """

    token: str = Field(validation_alias="BOT_TOKEN", default="")
    owner_ids: Set[int] = Field(validation_alias="OWNER_IDS", default_factory=set)

    @field_validator("owner_ids", mode="before")
    @classmethod
    def parse_owner_ids(cls, v):
        if isinstance(v, (list, set, tuple)):
            return {int(x) for x in v}
        if isinstance(v, str):
            if not v.strip():
                return set()
            return {int(x.strip()) for x in v.split(",") if x.strip()}
        if isinstance(v, int):
            return {v}
        raise ValueError(f"Invalid OWNER_IDS value: {v!r}")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"
