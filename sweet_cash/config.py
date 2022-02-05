class Config:
    SECRET_KEY = ''

    DATABASE_URI = ''

    NALOG_RU_HOST = 'https://irkkt-mobile.nalog.ru:8888'
    NALOG_RU_CLIENT_SECRET = ''
    NALOG_RU_OS = 'Android'
    NALOG_RU_DEVICE_OS = 'iOS'
    NALOG_RU_DEVICE_ID = ''

    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_REGEX = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

    MIN_TRANSACTION_AMOUNT = 0
    MAX_TRANSACTION_AMOUNT = 999999999999

    SMTP_HOST = 'smtp.yandex.ru'
    SMTP_PORT = 465
    EMAIL_ADDRESS = ''
    EMAIL_PASSWORD = ''
