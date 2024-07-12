from PIL import Image
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import WARNING_MEME_NOT_FOUND, WARNING_FILE_NOT_IMAGE
from app.crud.memes import get_by_id
from app.models import Memes


async def check_meme_exist(
    meme_id: int,
    session: AsyncSession
) -> Memes:
    meme_db = await get_by_id(meme_id, session)
    if meme_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=WARNING_MEME_NOT_FOUND.format(meme_id)
        )
    return meme_db


def check_image(file):
    try:
        Image.open(file)
    except OSError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=WARNING_FILE_NOT_IMAGE
        )
