from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_project_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверяем на уникальность имя проекта."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists_and_opened(
        project_id: int,
        session: AsyncSession,
        from_delete: bool = False
) -> CharityProject:
    """Проверяем, существует ли проект в БД."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    if charity_project.fully_invested:
        detail = 'Закрытый проект нельзя редактировать!'
        if from_delete:
            detail = 'В проект были внесены средства, не подлежит удалению!'
        raise HTTPException(
            status_code=400,
            detail=detail
        )
    return charity_project


async def check_project_is_empty(
        project_id: int,
        session: AsyncSession,
) -> None:
    """Проверяем, есть ли инвестиции в проекте."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_project_before_edit(
        project_id: int,
        new_full_amount: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверяем новую целевую сумму."""
    charity_project = await charity_project_crud.get(project_id, session)
    if new_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Новая сумма не может быть меньше уже внесенных средств!'
        )
    return charity_project
