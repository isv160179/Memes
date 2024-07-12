

# Memes

## Описание

Приложение на FastAPI, которое предоставляет API для работы с коллекцией мемов.
Приложение состоит из двух сервисов:

- сервис с публичным API с бизнес-логикой
- сервис для работы с медиа-файлами, используя S3-совместимое хранилище (MinIO).

### Функциональность:

- GET /memes: Получить список всех мемов (с пагинацией).
- GET /memes/{id}: Получить конкретный мем по его ID.
- POST /memes: Добавить новый мем (с картинкой и текстом).
- PUT /memes/{id}: Обновить существующий мем.
- DELETE /memes/{id}: Удалить мем.

### Примеры запросов и документация по API

Примеры запрсов и вся спецификация проекта представлена на странице http://127.0.0.1:8000/docs.
Документация отобразится в формате Swagger.

#### Ограничения определяемые в файле app/core/constrants.py

- Длина текста мема (LENGTH_TITLE) - 500 символов
- Длина имени файла (LENGTH_FILE_NAME) - 250 символов

#### Особенности при выполнеии запросов

- GET-запрос на получение всех мемов.
  Параметры пагинации:
    - Page - какую страницу вывести
    - Size - количество мемов на одной странице

- POST-запрос на публикацию мема.
    - Все поля (текст мема и его картинка) являются обязательными к заполнению.
    - Картинка сохраняется в хранилище MinIO под своим именем с префиксом текущего времени.

- GET-запрос на получение мема по ID.
    - При успешном нахождении мема по заданому ID, в папку проекта downloads (в докер-контейнере том -
      docker_download_files) скачивается файл, который соответствует данному мему.

## Запуск проекта

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:isv160179/test_madsoft.git
```

### Подготовка проекта к тестированию и запуску локально

- Перейти в каталог с проектом, скопировать в него содержимое .env.local в новый файл .env

```
cp .env.local .env
```

- Создать и активировать виртуальное окружение

```
python3 -m venv venv
source venv/bin/activate
```

- Установить зависимости

```
pip install -U pip
pip install -r requirements.txt
```

- Выполнить миграции

```
alembic upgrade head 
```

#### Запустить контейнер с сервисом MinIO (GNU/Linux and macOS)

```
mkdir -p ~/minio/data
docker run \
  -p 9000:9000 \
  -p 9001:9001 \
  --name minio-local \
  -v ~/minio/data:/data \
  -e "MINIO_ROOT_USER=minIOAdmin" \
  -e "MINIO_ROOT_PASSWORD=pass_MinIO@Admin" \
  quay.io/minio/minio server /data --console-address ":9001"
```

#### Запустить контейнер с сервисом MinIO (Windows)

```
docker run \
  -p 9000:9000 \
  -p 9001:9001 \
  --name minio-local \
  -v D:\data:/data \
  -e "MINIO_ROOT_USER=minIOAdmin" \
  -e "MINIO_ROOT_PASSWORD=pass_MinIO@Admin" \
  quay.io/minio/minio server /data --console-address ":9001"
```

- Перейти в web-интерфейс MinIO

```
http://127.0.0.1:9001  
```

- Создать хранилище (Create Bucket) с именем 'memes'

### Провести тестирование проекта

- Находясь в корневой папке проекта запустить тестирование

```
pytest
```

### Запуск проект локально

```
uvicorn app.main:app --reload
```

### Запуск проект в контейнерах

- Перейти в каталог с проектом, скопировать в него содержимое .env.docker в новый файл .env

```
cp .env.docker .env
```

- Перейти в каталог с файлом docker-compose.yaml

```
cd docker
```

- Запустить docker-compose.yaml

```
docker compose up
```

- После успешного запуска всех контейнеров выполнить миграции находясь в папке docker:

```
docker compose exec memes alembic upgrade head
```

## Перейти на страницу с API документации Swagger:

```
http://127.0.0.1:8000/docs#
```
## Стек технологий
  - Python
  - FastAPI
  - Uvicorn
  - Pydantic
  - MinIO
  - PostgreSQL
  - SQLite
  - Alembic
  - Docker
  - Pytest
 