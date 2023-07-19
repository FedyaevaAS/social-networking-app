# Проект: API для социальной сети

### Описание функционала приложения
* Пользователь может зарегистрироваться и залогиниться
* Пользователь может создавать, редактировать, удалять и просматривать посты
* Пользователь может оставлять лайки на посты других пользователей

### Стек технологий Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Asyncio
- nginx
- gunicorn
- Docker

### Начало работы
Клонируйте репозиторий и перейдите в него в командной строке:
```
https://github.com/FedyaevaAS/social-networking-app
```
### Запуск проекта локально
- Установите Docker, используя инструкции с официального сайта:
https://www.docker.com/products/docker-desktop/
- Создайте файл .env в корне проекта со следующим содержимым:
    ```
    APP_TITLE=Социальная сеть # Название приложение
    POSTGRES_DB=social_network_db # Название базы данных
    POSTGRES_USER=postgres  # Логин для подключения к базе данных
    POSTGRES_PASSWORD=postgres  # Пароль для подключения к базе данных
    DB_HOST=localhost  # Название сервиса (контейнера)
    DB_PORT=5432  # Порт для подключения к базе данных
    SECRET=SOMEWORD # Cекретное слово для генерации jwt-токенов
    ```
- В корневой директории выполните команды для запуска приложения в контейнерах

    - Собрать и запустить контейнеры:
        ```
        docker-compose up -d --build
        ```
    - Выполнить миграции:
        ```
        docker-compose exec backend alembic upgrade head
        ```
    - Остановить контейнеры:
        ```
        docker-compose down -v 
        ```
### Ссылки на автоматически сгенерированную документацию:
- http://localhost/docs - Swagger
- http://localhost/redoc - ReDoc
### Автор
Федяева Анастасия
