# ✨ Backend Fastapi

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.10.2-green.svg?logo=pydantic&logoColor=white)](https://pydantic.dev/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.32.1-f7614d.svg?logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)
[![GitHub stars](https://img.shields.io/github/stars/blackgyana/backend-fastapi?style=social)](https://github.com/blackgyana/backend-fastapi/stargazers)

> Этот репозиторий содержит базовый backend API-сервис, разработанный с использованием высокопроизводительного фреймворка FastAPI на Python.

---

## ✨ Основные возможности

Проект, несмотря на свою компактность, реализует лучшие практики для построения надежного и эффективного backend API:

*   **Высокопроизводительный API:** Использует FastAPI для создания эффективных и масштабируемых RESTful-эндпоинтов с автоматической валидацией данных и сериализацией/десериализацией.
*   **Надежная валидация данных:** Применяет Pydantic для определения строгих моделей данных, обеспечения целостности входных данных и надежной проверки структуры данных.
*   **Гибкая конфигурация окружения:** Управление чувствительными данными и конфигурациями окружений через файл `.env` с использованием `python-dotenv`.
*   **Асинхронный gateway-сервер:** Основан на Uvicorn — быстром ASGI-сервере для обслуживания API с поддержкой асинхронности и эффективного использования возможностей Python.
*   **Валидация email-адресов:** Интеграция `email_validator` для корректной обработки и проверки email-адресов.
*   **Удобные CLI-инструменты для разработчиков:** Используются `fastapi-cli` и `Typer` для улучшения процесса разработки и работы из командной строки.

## 🛠️ Технологический стек

Проект построен на современном и эффективном технологическом стеке:

| Категория               | Технология          | Примечание                                                             |
| :---------------------- | :------------------ | :---------------------------------------------------------------------- |
| **Язык программирования** | Python              | Основной язык для backend-логики и разработки API.                     |
| **Веб-фреймворк**        | FastAPI             | Высокопроизводительный веб-фреймворк для создания RESTful API.         |
| **Валидация данных**     | Pydantic            | Используется для валидации данных, сериализации и управления настройками. |
| **ASGI-сервер**          | Uvicorn             | Очень быстрый ASGI-сервер для запуска приложений FastAPI.              |
| **Управление Env**       | python-dotenv       | Управление переменными окружения из файла `.env`.                      |
| **CLI-инструменты**      | fastapi-cli, Typer  | Упрощают разработку и взаимодействие через командную строку.           |
| **Валидация Email**      | email-validator     | Для проверки корректности формата email-адресов.                       |
| **HTTP-клиент**          | httpx               | Полностью асинхронный HTTP-клиент для Python.                          |

## 🏛️ Обзор архитектуры

Приложение использует простую и эффективную RESTful-архитектуру API, построенную вокруг фреймворка FastAPI. Оно спроектировано как самостоятельный backend-сервис, где `main.py` выступает в роли основной точки входа приложения. Такая архитектура способствует модульности, удобству тестирования и масштабируемости за счет разделения ответственности и четкой структуры эндпоинтов API. В качестве основного языка используется Python, что обеспечивает чистый и выразительный процесс разработки.

## 🚀 Начало работы

Следуйте этим шагам, чтобы запустить проект локально на вашем компьютере.

### Предварительные требования

Убедитесь, что у вас установлено следующее:

*   [Python 3.x](https://www.python.org/downloads/)
*   [pip](https://pip.pypa.io/en/stable/installation/) (обычно устанавливается вместе с Python)

### Установка

1.  **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/blackgyana/backend-fastapi.git
    cd backend-fastapi
    ```

2.  **Создайте и активируйте виртуальное окружение:**

    ```bash
    python -m venv venv
    # В Windows
    .\venv\Scripts\activate
    # В macOS/Linux
    source venv/bin/activate
    ```

3.  **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Запустите приложение FastAPI:**

    ```bash
    uvicorn main:app --reload
    ```
    Или, если вы хотите использовать CLI-инструмент FastAPI:
    ```bash
    fastapi dev
    ```

    Приложение будет доступно по адресу `http://127.0.0.1:8000`. Интерактивная документация API (Swagger UI) доступна по адресу `http://127.0.0.1:8000/docs`, а Redoc — по адресу `http://127.0.0.1:8000/redoc`.

## 📂 Структура файлов
├── .gitignore
├── main.py
└── requirements.txt

*   **`.gitignore`**: Определяет файлы и директории, которые должны игнорироваться Git.
*   **`main.py`**: Основной файл приложения, содержащий определение приложения FastAPI и API-эндпоинты.
*   **`requirements.txt`**: Список всех Python-зависимостей проекта, используемый для установки пакетов через `pip`.

----------------------------------------------------------------------------------------------------


docker network create booking-network

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=booking-network \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name booking_cache \
    -p 7379:6379 \
    --network=booking-network \
    -d redis:7.4

docker run --name booking_back \
    -p 8080:8000 \
    --network=booking-network \
    booking_image


docker run --name booking_celery_worker \
    --network=booking-network \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking_celery_beat \
    --network=booking-network \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B


docker build -t booking_image .


docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=booking-network \
    --rm -p 80:80 nginx
    --rm -p 80:80 -p 443:443 nginx


