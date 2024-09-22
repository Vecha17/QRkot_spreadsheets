from sqlalchemy import Column, String, Text

from .base import Invest


class CharityProject(Invest):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f'{super().__repr__()}, {self.name}, {self.description}'
