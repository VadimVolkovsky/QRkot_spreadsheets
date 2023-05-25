from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.config import (CREATE_AND_CLOSE_DATES_FORMAT,
                             EXAMPLE_FULL_AMOUNT, EXAMPLE_INVESTED_AMOUNT,
                             EXAMPLE_PROJECT_DESCRIPTION, EXAMPLE_PROJECT_NAME,
                             PROJECT_DESCRIPTION_MAX_LENGTH,
                             PROJECT_DESCRIPTION_MIN_LENGTH,
                             PROJECT_NAME_MAX_LENGTH, PROJECT_NAME_MIN_LENGTH)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH,
        example=EXAMPLE_PROJECT_NAME
    )
    description: Optional[str] = Field(
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH,
        max_length=PROJECT_DESCRIPTION_MAX_LENGTH,
        example=EXAMPLE_PROJECT_DESCRIPTION
    )
    full_amount: Optional[PositiveInt] = Field(example=EXAMPLE_FULL_AMOUNT)

    class Config():
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=100, example=EXAMPLE_PROJECT_NAME
    )
    description: str = Field(
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH,
        max_length=PROJECT_DESCRIPTION_MAX_LENGTH,
        example=EXAMPLE_PROJECT_DESCRIPTION
    )
    full_amount: PositiveInt = Field(example=EXAMPLE_FULL_AMOUNT)


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: Optional[int]
    invested_amount: Optional[int] = Field(example=EXAMPLE_INVESTED_AMOUNT)
    fully_invested: Optional[bool]
    create_date: Optional[datetime] = Field(example=CREATE_AND_CLOSE_DATES_FORMAT)
    close_date: Optional[datetime] = Field(example=CREATE_AND_CLOSE_DATES_FORMAT)

    class Config:
        orm_mode = True
