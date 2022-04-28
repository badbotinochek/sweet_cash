
import os
from dotenv import load_dotenv


load_dotenv(os.path.join('local.env'))


class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    DATABASE_URI: str = os.getenv("DATABASE_URI")

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: str = os.getenv("REDIS_PORT")
    REDIS_DB: str = os.getenv("REDIS_DB")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")

    NALOG_RU_HOST: str = os.getenv("NALOG_RU_HOST")
    NALOG_RU_CLIENT_SECRET: str = os.getenv("NALOG_RU_CLIENT_SECRET")
    NALOG_RU_OS: str = os.getenv("NALOG_RU_OS")
    NALOG_RU_DEVICE_OS: str = os.getenv("NALOG_RU_DEVICE_OS")
    NALOG_RU_DEVICE_ID: str = os.getenv("NALOG_RU_DEVICE_ID")

    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: str = os.getenv("SMTP_PORT")
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")

    SWEET_CASH_URL = 'http://bsikpg.duckdns.org'

    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_REGEX = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

    MIN_TRANSACTION_AMOUNT = 0
    MAX_TRANSACTION_AMOUNT = 999999999999

    JWT_EXPIRE_TIME = 24

    DEBUG = True

    EVENT_PROCESSORS = ['Processor-1']
    EVENT_LISTENING_PERIOD_IN_SECONDS = 10
    