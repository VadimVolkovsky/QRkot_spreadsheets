from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):
    async def get_by_user(
            self,
            user: User,
            session: AsyncSession
    ):
        """Возвращает список пожертвований сделанных пользователем"""
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()

    async def find_donations_for_project(
        self,
        charity_project,
        session: AsyncSession,
    ):
        """Ищет подходящие для проекта донаты"""
        donations = await session.execute(
            select(Donation).where(
                and_(Donation.full_amount <= charity_project.full_amount,
                     Donation.fully_invested == False) # noqa
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
