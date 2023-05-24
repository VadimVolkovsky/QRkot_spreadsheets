from datetime import timedelta
from typing import Dict, List, Union

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.models.donation import Donation


class CRUDCharityProject(CRUDBase):
    async def find_project_for_investments(
            self,
            donation: Donation,
            sesssion: AsyncSession,
    ):
        """Ищет открытый проект, в который можно вложить указанную сумму денег"""
        charity_projects = await sesssion.execute(
            select(CharityProject).where(
                (CharityProject.full_amount - CharityProject.invested_amount) >= donation.full_amount
            )
        )
        return charity_projects.scalars().first()

    async def get_charity_project_by_name(
            self,
            charity_project,
            session: AsyncSession
    ):
        """Ищет в БД проект по его названию"""
        charity_project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == charity_project.name
            )
        )
        return charity_project.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> List[Dict[str, Union[timedelta, str]]]:
        """Получате из БД список всех закрытых проектов
        и сортирует по времени закрытия"""
        closed_projects = await session.execute(
            select([CharityProject.name,
                    (func.julianday(CharityProject.close_date) - func.julianday(CharityProject.create_date)).label('timediff'),
                    CharityProject.description]).where(
                CharityProject.fully_invested == 1
            ).order_by('timediff')
        )
        return closed_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
