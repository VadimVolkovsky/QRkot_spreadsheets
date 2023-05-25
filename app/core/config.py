import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, EmailStr

CREATE_AND_CLOSE_DATES_FORMAT = datetime.today().strftime("%Y-%m-%dT%H:%M")
PROJECT_NAME_MIN_LENGTH = 5
PROJECT_NAME_MAX_LENGTH = 100
PROJECT_DESCRIPTION_MIN_LENGTH = 5
PROJECT_DESCRIPTION_MAX_LENGTH = 1000
DONATION_FULL_AMOUNT_MIN_VALUE = 0
EXAMPLE_PROJECT_NAME = 'Рыжий кот'
EXAMPLE_PROJECT_DESCRIPTION = 'Сбор денег для рыжих котов'
EXAMPLE_FULL_AMOUNT = 5000
EXAMPLE_INVESTED_AMOUNT = 2500

BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / 'logs'
LOG_FILE = LOGS_DIR / 'fastapi_app.log'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DR_FORMAT = '%d.%m.%Y %H:%M:%S'


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд - QRKot'
    app_description: str = 'Задонать котику'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()


def configure_logging():
    """Описание конфигурации для логирования"""
    LOGS_DIR.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10**6, backupCount=5, encoding='utf-8'
    )

    logging.basicConfig(
        datefmt=DR_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler,)
    )
