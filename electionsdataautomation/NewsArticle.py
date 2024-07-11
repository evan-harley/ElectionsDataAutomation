from datetime import datetime
from sqlalchemy import String
from sqlalchemy import types
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import uuid


class Base(DeclarativeBase):
    pass


class NewsArticle(Base):

    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    publisher_url: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()