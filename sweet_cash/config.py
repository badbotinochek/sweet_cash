class Config:
    SECRET_KEY = '025b376adf584b72888bffe69f90524d'

    DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/postgres'
    # DATABASE_URI = 'postgresql://postgres:911911@app_pg:5432/postgres'

    NALOG_RU_HOST = 'https://irkkt-mobile.nalog.ru:8888'
    NALOG_RU_CLIENT_SECRET = 'IyvrAbKt9h/8p6a7QPh8gpkXYQ4='
    NALOG_RU_OS = 'Android'
    NALOG_RU_DEVICE_OS = 'iOS'
    NALOG_RU_DEVICE_ID = '7C82010F-16CC-446B-8F66-FC4080C66522'

    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_REGEX = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

    MIN_TRANSACTION_AMOUNT = 0
    MAX_TRANSACTION_AMOUNT = 999999999999

    SMTP_HOST = 'smtp.yandex.ru'
    SMTP_PORT = 465
    EMAIL_ADDRESS = 'dka45-1p@yandex.ru'
    EMAIL_PASSWORD = 'qbrosrbmvqepucsn'
