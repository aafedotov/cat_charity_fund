from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class MeetingRoomDB(CharityProjectCreate):
    id: int
    invested_amount: PositiveInt = 0
    fully_invested: bool = False
    create_date: datetime = datetime.now()
    close_date: datetime

    class Config:
        orm_mode = True
