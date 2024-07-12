from pydantic import BaseSettings

from app.core.constants import (
    APP_TITLE,
    APP_DESCRIPTION,
    DATABASE_URL,
    MINIO_URL,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET, TEST_DATABASE_URL, DOWNLOAD_DIR,
)


class Settings(BaseSettings):
    app_title: str = APP_TITLE
    app_description: str = APP_DESCRIPTION
    database_url: str = DATABASE_URL
    test_database_url: str = TEST_DATABASE_URL
    minio_url: str = MINIO_URL
    minio_access_key: str = MINIO_ACCESS_KEY
    minio_secret_key: str = MINIO_SECRET_KEY
    minio_bucket: str = MINIO_BUCKET
    download_dir: str = DOWNLOAD_DIR
    class Config:
        env_file = '.env'


settings = Settings()
