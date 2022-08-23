from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import(
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB,
)
from app.core.user import current_superuser
from app.api.validators import (
    check_project_name_duplicate,
    check_project_exists,
    check_full_amount_before_edit,
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    # response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_project_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    # response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_project_exists(project_id, session)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_project_exists(project_id, session)
    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        charity_project = await check_full_amount_before_edit(
            project_id,
            obj_in.full_amount,
            session
        )
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project

#
#
# @router.get(
#     '/{meeting_room_id}/reservations',
#     response_model=list[ReservationDB],
#     response_model_exclude={'user_id'},
# )
# async def get_reservations_for_room(
#         meeting_room_id: int,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     await check_meeting_room_exists(meeting_room_id, session)
#     reservations = await crud_reservation.get_future_reservations_for_room(
#         room_id=meeting_room_id, session=session
#     )
#     return reservations
#
#
# @router.patch(
#     '/{meeting_room_id}',
#     response_model=MeetingRoomDB,
#     response_model_exclude_none=True,
#     dependencies=[Depends(current_superuser)],
# )
# async def partially_update_meeting_room(
#         meeting_room_id: int,
#         obj_in: MeetingRoomUpdate,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     meeting_room = await check_meeting_room_exists(
#         meeting_room_id, session
#     )
#
#     if obj_in.name is not None:
#         await check_name_duplicate(obj_in.name, session)
#
#     meeting_room = await meeting_room_crud.update(
#         meeting_room, obj_in, session
#     )
#     return meeting_room
#
#
# @router.delete(
#     '/{meeting_room_id}',
#     response_model=MeetingRoomDB,
#     response_model_exclude_none=True,
#     dependencies=[Depends(current_superuser)],
# )
# async def remove_meeting_room(
#         meeting_room_id: int,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     meeting_room = await check_meeting_room_exists(meeting_room_id, session)
#     meeting_room = await meeting_room_crud.remove(meeting_room, session)
#     return meeting_room