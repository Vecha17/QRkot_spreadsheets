from sqlalchemy import Column, String, Text

from .base import QRKotBaseModel


class CharityProject(QRKotBaseModel):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return super().__repr__()
