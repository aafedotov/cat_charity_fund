from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base


class CharityProject(Base):
    """Модель для проектов для пожертвований."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now())
    close_date = Column(DateTime)