from sqlalchemy import Column, String, Text

from app.core.db import Base, ProjectDonationABC


class CharityProject(Base, ProjectDonationABC):
    """Модель создания проекта для пожертвований"""
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
