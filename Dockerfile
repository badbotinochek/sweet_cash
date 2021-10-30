## установка базового образа (host OS)
#FROM python:3.7
#
## установка рабочей директории в контейнере
#WORKDIR /code
#
## копирование файла зависимостей в рабочую директорию
#COPY requirements.txt .
#
## установка зависимостей
#RUN pip install -r requirements.txt
#
## копирование содержимого локальной директории в рабочую директорию
#COPY /sweet_cash .
#
#EXPOSE 5000
#
## команда, выполняемая при запуске контейнера
#CMD [ "python", "./app.py" ]


# первый этап
FROM python:3.7 AS builder

# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .

# установка зависимостей в локальную директорию user (например, /root/.local)
RUN pip install --user -r requirements.txt

# второй этап (без названия)
FROM python:3.7

# установка рабочей директории в контейнере
WORKDIR /code

# копирование только установки зависимостей из образа первого этапа
COPY --from=builder /root/.local /root/.local

# копирование содержимого локальной директории в рабочую директорию
COPY ./sweet_cash .

# обновление переменной среды PATH
ENV PATH=/root/.local:$PATH

# команда, выполняемая при запуске контейнера
CMD [ "python", "./app.py" ]