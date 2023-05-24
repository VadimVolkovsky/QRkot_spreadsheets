from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def check_project_name_is_unique(
        charity_project,
        session: AsyncSession
):
    """Проверяет уникальность имени проекта"""
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project,
        session
    )
    if charity_project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_before_edit(
        project_id,
        obj_in,
        session: AsyncSession,
):
    """Проверяет проект перед редактированием"""
    charity_project = await charity_project_crud.get(
        project_id,
        session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Проект не найден'
        )
    check_project_is_fully_invested(charity_project)
    if obj_in.name is not None:
        await check_project_name_is_unique(charity_project=obj_in, session=session)
    if obj_in.full_amount is not None:
        check_project_full_amount_field(charity_project, obj_in)
    return charity_project


def check_project_is_fully_invested(
    charity_project,
):
    """Проверяет, что проект не закрыт"""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_project_full_amount_field(
    charity_project,
    obj_in,
):
    """Проверяет что необходимая сумма не меньше уже вложенной суммы"""
    if obj_in.full_amount is not None:
        if obj_in.full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Нельзя установить требуемую сумму меньше уже вложенной'
            )


async def check_project_before_delete(
        project_id,
        session: AsyncSession
):
    """Проверяет проект перед удалением"""
    charity_project = await charity_project_crud.get(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Проект не найден'
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project
