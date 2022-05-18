import os
from dotenv import load_dotenv

load_dotenv(os.path.join('local.env'))


class TestConfig:
    HOST: str = os.getenv("HOST")
    NAME: str = os.getenv("NAME")
    EMAIL: str = os.getenv("EMAIL")
    PHONE: str = os.getenv("PHONE")
    PASSWORD: str = os.getenv("PASSWORD")
    TOKEN: str = os.getenv("TOKEN")


