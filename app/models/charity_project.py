from sqlalchemy import Column, String, Text

from .base import AppBase


class CharityProject(AppBase):
    """Модель для проектов для пожертвований."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
