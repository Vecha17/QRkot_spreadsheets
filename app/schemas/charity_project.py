from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.consts import (
    NAME_MAX_LENGTH, NAME_MIN_LENGTH
)


class CharityProjectBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH
    )
    description: str
    full_amount: int = Field(..., gt=0)

    @validator('name')
    def validate_name(cls, value):
        if not value:
            raise ValueError('Проект должен содержать имя!')
        return value

    @validator('description')
    def validate_description(cls, value):
        if not value:
            raise ValueError('Проект должен содержать описание!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: Optional[int] = Field(...,)
    fully_invested: Optional[bool] = Field(...,)
    create_date: datetime
    close_date: Optional[datetime] = Field(...,)

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):

    class Config:
        extra = Extra.forbid
