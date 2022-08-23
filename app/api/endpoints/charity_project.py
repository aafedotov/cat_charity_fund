from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.investment import project_processing
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
    check_project_exists_and_opened,
    check_project_before_edit,
    check_project_is_empty,
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
    new_project = project_processing(new_project, session)
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
    charity_project = await check_project_exists_and_opened(
        project_id, session
    )
    await check_project_is_empty(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
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
    charity_project = await check_project_exists_and_opened(
        project_id, session
    )
    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        charity_project = await check_project_before_edit(
            project_id,
            obj_in.full_amount,
            session
        )
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    charity_project = await project_processing(charity_project, session)
    return charity_project
