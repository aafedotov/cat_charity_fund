from sqlalchemy import Column, Text, Integer, ForeignKey

from .base import AppBase


class Donation(AppBase):
    """Модель для пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
