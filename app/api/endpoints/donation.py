from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.user import User
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB
from app.core.user import current_superuser, current_user
from app.api.validators import (
    check_project_name_duplicate,
    check_project_exists,
    check_full_amount_before_edit,
)

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date'
    },
)
async def create_donation(
        reservation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(reservation, session, user)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date'
    },
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    user_donations = await donation_crud.get_by_user(session, user)
    return user_donations
