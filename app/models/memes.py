from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime

from app.core.constants import LENGTH_FILE_NAME
from app.core.db import Base


class Memes(Base):
    title = Column(Text, nullable=False)
    file_name = Column(String(LENGTH_FILE_NAME), nullable=False)
    create_date = Column(DateTime, default=datetime.now)
