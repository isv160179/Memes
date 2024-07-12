from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field, Extra

from app.core.constants import LENGTH_FILE_NAME, LENGTH_TITLE


class MemesBase(BaseModel):
    title: Annotated[
        Optional[str],
        Field(min_length=1, max_length=LENGTH_TITLE)
    ] = None
    file_name: Annotated[
        Optional[str],
        Field(min_length=1, max_length=LENGTH_FILE_NAME)
    ] = None

    class Config:
        extra = Extra.forbid


class MemesDB(MemesBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
