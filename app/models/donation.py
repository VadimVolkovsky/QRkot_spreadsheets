from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, ProjectDonationABC


class Donation(Base, ProjectDonationABC):
    """Модель для создания пожертвования"""
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('donation.id'))
