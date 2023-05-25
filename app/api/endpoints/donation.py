from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.invest import commit_investments_in_db, invest_to_project

router = APIRouter()


@router.get(
    '/donation/',
    dependencies=[Depends(current_superuser)],
    response_model=List[DonationDB]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Получает список всех пожертвований - только для суперюзеров"""
    return await donation_crud.get_multi(session)


@router.get(
    '/donation/my',
    dependencies=[Depends(current_user)],
    response_model=List[DonationDB],
    response_model_exclude=('user_id', 'invested_amount', 'fully_invested', 'close_date')
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_by_user(user, session)


@router.post(
    '/donation/',
    dependencies=[Depends(current_user)],
    response_model=DonationDB,
    response_model_exclude=('user_id', 'invested_amount', 'fully_invested'),
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создает новое пожертвование"""
    donation = await donation_crud.create(
        donation,
        session,
        user
    )
    charity_project = await charity_project_crud.find_project_for_investments(
        donation,
        session,
    )
    if charity_project is not None:
        charity_project, donation, session = await invest_to_project(charity_project, donation, session)
        charity_project, donation = await commit_investments_in_db(charity_project, donation, session)
    return donation
