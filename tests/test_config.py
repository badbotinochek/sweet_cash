import os
from dotenv import load_dotenv

load_dotenv(os.path.join('local.env'))


class Config:
    HOST: str = os.getenv("HOST")
    NAME: str = os.getenv("HOST")
    EMAIL: str = os.getenv("HOST")
    PHONE: str = os.getenv("HOST")
    PASSWORD: str = os.getenv("HOST")

