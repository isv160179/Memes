from typing import Annotated

from PIL import Image
from fastapi import APIRouter, UploadFile, Form, Query, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meme_exist, check_image
from app.core.config import settings
from app.core.db import get_async_session
from app.crud.memes import create, get_all, delete, update
from app.crud.minio import MinioHandler
from app.models import Memes
from app.shemas.memes import MemesDB

router = APIRouter()

minio_handler = MinioHandler(
    settings.minio_url,
    settings.minio_access_key,
    settings.minio_secret_key,
    settings.minio_bucket,
    False
)


@router.post(
    '/',
    summary='Создание мема',
)
async def create_meme(
    file: Annotated[UploadFile, Form()],
    text: str = Query(
        ...,
        min_length=2,
        max_length=500,
        description='Текст нового мема.'
    ),
    session: AsyncSession = Depends(get_async_session),
):
    check_image(file.file)
    file_name = await minio_handler.upload_file(file)
    new_obj_dict = {
        'title': text,
        'file_name': file_name,
    }
    return await create(new_obj_dict, session)


@router.get(
    '/',
    response_model=Page[MemesDB],
    response_model_exclude_none=True,
)
async def get_all_memes(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех мемов с пагинацией."""
    return paginate(await get_all(session))


@router.get(
    '/{meme_id}',
    response_model=MemesDB,
    response_model_exclude_none=True
)
async def get_by_id(
    meme_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Memes:
    """Возвращает мем по его ID."""
    meme = await check_meme_exist(meme_id, session)
    path = settings.download_dir
    await minio_handler.get(meme.file_name, path)
    return meme


@router.delete(
    '/{meme_id}',
    response_model=MemesDB
)
async def delete_meme(
    meme_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляет мем по его ID.
    """
    meme_db = await check_meme_exist(meme_id, session)
    await minio_handler.delete(meme_db.file_name)
    return await delete(meme_db, session)


@router.put(
    '/{meme_id}',
    summary='Изменение мема',
)
async def update_meme(
    meme_id: int,
    file: Annotated[UploadFile, Form()] = None,
    text: str = Query(
        None,
        min_length=2,
        max_length=500,
        description='Текст мема.'
    ),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Изменение мема.
    """
    new_obj_dict = {}
    meme_db = await check_meme_exist(meme_id, session)
    if file is not None:
        await minio_handler.delete(meme_db.file_name)
        file_name = await minio_handler.upload_file(file)
        new_obj_dict = {
            'file_name': file_name,
        }
    if text is not None:
        new_obj_dict['title'] = text
    return await update(meme_db, new_obj_dict, session)
