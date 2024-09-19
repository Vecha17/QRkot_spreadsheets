from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationGetAll(DonationDB):
    user_id: int
    invested_amount: Optional[int] = Field(...)
    fully_invested: Optional[bool] = Field(...)
    close_date: Optional[datetime] = Field(...)
