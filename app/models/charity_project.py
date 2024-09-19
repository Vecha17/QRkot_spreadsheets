from sqlalchemy import Column, String, Text

from app.core.db import Base

from .base import BaseModel


class CharityProject(Base, BaseModel):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
