# Snaily

## Описание

Веб-приложение task manager использующее систему мотивации и поощрений для ежедневного выполнения задач

## Установка

1. Клонируйте репозиторий:

```sh
    git clone https://github.com/snaily418/back/
    cd back
```

2. Создайте и активируйте виртуальное окружение:

```sh
   python -m venv venv
   venv/Scripts/activate
```

3. Установите все зависимости:

```sh
   pip install -r requirements.txt
```

### Используемые библиотеки

1. FastAPI
2. Bcrypt
3. Pydantic
4. SQLAlchemy
5. APScheduler
6. Uvicorn

## Запуск приложения

Это ASGI приложение и запускается с помощью сервера uvicorn автоматически. Просто запустите `main.py`

```sh
python main.py
```

## Тестирование

Чтобы проверить, что приложение работает, откройте браузер и перейдите по адресу:

http://127.0.0.1:8000/
Вы должны увидеть в ответ `pong`.

Смена дня будет выполняться каждый день в 1:00 ночи.

# Команда проекта

Миша - Front Engineer \
Родион - Front Engineer \
Коля - Team Lead \
Даня - Backend Engineer \
Гоша - Project Manager
