from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cache_capacity: int = 100
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(levelname)s - %(message)s"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(yellow)s%(asctime)s%(reset)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "blue",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": "../logs/app.log",
            "mode": "a",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
