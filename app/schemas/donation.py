from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.core.config import DONATION_FULL_AMOUNT_MIN_VALUE


class DonationCreate(BaseModel):
    full_amount: int = Field(gt=DONATION_FULL_AMOUNT_MIN_VALUE)
    comment: Optional[str]

    class Config():
        extra = Extra.forbid


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool

    class Config:
        orm_mode = True
