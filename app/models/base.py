from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class Invest(Base):
    __abstract__ = True
    full_amount = Column(Integer, CheckConstraint('full_amount > 0'))
    invested_amount = Column(
        Integer,
        CheckConstraint('0 <= invested_amount <= full_amount'),
        default=0
    )
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)

    def __repr__(self) -> str:
        return (
            f'{self.full_amount=}, {self.invested_amount=},'
            f' {self.fully_invested=}, {self.create_date=}, {self.close_date=}'
        )
