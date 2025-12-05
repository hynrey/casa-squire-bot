from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    log_level: str = Field(default="DEBUG", validation_alias="LOG_LEVEL")
