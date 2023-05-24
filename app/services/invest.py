from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession


async def update_donation(donation):
    """Обновляет статус пожертвования"""
    donation.invested_amount = donation.full_amount
    donation.fully_invested = True
    donation.close_date = datetime.now()
    return donation


async def update_project(charity_project, donation):
    """Обновляет статус проекта. Закрывает проект, если собрана необходимая сумма"""
    charity_project.invested_amount += donation.full_amount
    if charity_project.full_amount == charity_project.invested_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now()
    return charity_project


async def invest_to_project(
        charity_project,
        donation,
        session: AsyncSession,
):
    """Инвестируем донаты в проект"""
    donation = await update_donation(donation)
    charity_project = await update_project(charity_project, donation)
    session.add(donation)
    session.add(charity_project)
    return charity_project, donation, session


async def invest_donations_in_new_project(
        charity_project,
        donations,
        session: AsyncSession
):
    """Инвестирует подходящие донаты в только что созданный проект"""
    invested_amount = 0
    for donation in donations:
        if (invested_amount + donation.full_amount) <= charity_project.full_amount:
            charity_project, donation, session = await invest_to_project(charity_project, donation, session)
            invested_amount += donation.full_amount
    charity_project, donation = await commit_investments_in_db(charity_project, donation, session)


async def commit_investments_in_db(
    charity_project,
    donation,
    session: AsyncSession
):
    await session.commit()
    await session.refresh(donation)
    await session.refresh(charity_project)
    return charity_project, donation
