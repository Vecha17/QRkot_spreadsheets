from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import Invest


class Donation(Invest):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return f'{super().__repr__()}, {self.user_id=}, {self.comment=}'
