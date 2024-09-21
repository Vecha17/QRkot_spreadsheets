from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import QRKotBaseModel


class Donation(QRKotBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return super().__repr__()
