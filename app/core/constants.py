APP_TITLE = 'Memes'
APP_DESCRIPTION = 'Collection of app'
DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
TEST_DATABASE_URL = 'sqlite+aiosqlite:///test.db'
MINIO_URL = 'MINIO_URL'
MINIO_ACCESS_KEY = 'ACCESS_KEY'
MINIO_SECRET_KEY = 'SECRET_KEY'
MINIO_BUCKET = 'BUCKET'
DOWNLOAD_DIR = './downloads/'
LENGTH_FILE_NAME = 250
LENGTH_TITLE = 500
TITLE_ERR = "Название мема не может быть пустым!"
WARNING_MEME_NOT_FOUND = "Мем с ID = {} не найден!"
WARNING_FILE_NOT_IMAGE = "Загружаемый файл не вляется изображением!"