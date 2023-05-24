from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_project_before_delete,
                                check_project_before_edit,
                                check_project_name_is_unique)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.invest import invest_donations_in_new_project

router = APIRouter()


@router.get(
    '/charity_project/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_charity_project(
    session: AsyncSession = Depends(get_async_session)
):
    """Получает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/charity_project/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создает проект для пожертвований"""
    await check_project_name_is_unique(charity_project, session)
    charity_project = await charity_project_crud.create(
        charity_project,
        session
    )
    donations = await donation_crud.find_donations_for_project(
        charity_project,
        session
    )
    if donations:
        await invest_donations_in_new_project(
            charity_project,
            donations,
            session
        )
    return charity_project


@router.delete(
    '/charity_project/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление проекта пожертвований"""
    charity_project = await check_project_before_delete(project_id, session)
    return await charity_project_crud.remove(charity_project, session)


@router.patch(
    '/charity_project/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_project_before_edit(project_id, obj_in, session)
    charity_project = await charity_project_crud.update(
        charity_project,
        obj_in,
        session
    )
    return charity_project
