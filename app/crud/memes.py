from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Memes


async def get_all(session: AsyncSession) -> List[Memes]:
    db_objs = await session.scalars(select(Memes))
    return db_objs.all()


async def get_by_id(
    meme_id: int,
    session: AsyncSession
) -> Optional[Memes]:
    return await session.get(Memes, meme_id)


async def create(
    new_obj_dict: dict,
    session: AsyncSession
) -> Memes:
    new_obj_db = Memes(**new_obj_dict)
    session.add(new_obj_db)
    await session.commit()
    await session.refresh(new_obj_db)
    return new_obj_db


async def update(
    meme_db: Memes,
    new_obj_dict: dict,
    session: AsyncSession,
) -> Memes:
    dict_from_db = jsonable_encoder(meme_db)
    for field in dict_from_db:
        if field in new_obj_dict:
            setattr(meme_db, field, new_obj_dict[field])
    session.add(meme_db)
    await session.commit()
    await session.refresh(meme_db)
    return meme_db


async def delete(
    memes_db: Memes,
    session: AsyncSession,
) -> Memes:
    await session.delete(memes_db)
    await session.commit()
    return memes_db
