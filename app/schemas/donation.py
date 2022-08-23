from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, root_validator, validator, Extra, Field, PositiveInt


class DonationCreate(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate):
    id: int
    user_id: Optional[int]
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: datetime = datetime.now()
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
