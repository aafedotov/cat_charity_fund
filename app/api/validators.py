from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import User, CharityProject


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
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверяем, существует ли проект в БД."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_full_amount_before_edit(
        project_id: int,
        new_full_amount: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверяем новую целевую сумму (не менее текущих донатов на проект)."""
    charity_project = await charity_project_crud.get(project_id, session)
    if new_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Новая сумма не может быть меньше уже внесенных средств!'
        )
    return charity_project

#
#
# async def check_reservation_intersections(**kwargs) -> None:
#     reservations = await crud_reservation.get_reservations_at_the_same_time(
#         **kwargs
#     )
#     if reservations:
#         raise HTTPException(
#             status_code=422,
#             detail=str(reservations)
#         )
#
#
# async def check_reservation_before_edit(
#         reservation_id: int,
#         session: AsyncSession,
#         user: User,
# ) -> Reservation:
#     reservation = await crud_reservation.get(reservation_id, session)
#     if reservation is None:
#         raise HTTPException(
#             status_code=404,
#             detail='Бронь не найдена!'
#         )
#     if not user.is_superuser and reservation.user_id != user.id:
#         raise HTTPException(
#             status_code=403,
#             detail='Невозможно редактировать или удалить чужую бронь!'
#         )
#     return reservation