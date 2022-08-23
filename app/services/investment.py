from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User, CharityProject, Donation


async def project_processing(
        charity_project: CharityProject,
        session: AsyncSession
) -> CharityProject:
    """Процессинг инвестиций при додавлении или изменении проектов."""

    free_donations = await donation_crud.get_free_donations(session)
    to_invest = charity_project.full_amount - charity_project.invested_amount
    if to_invest == 0:
        return charity_project
    for donation in free_donations:
        to_donate = donation.full_amount - donation.invested_amount
        if to_donate < to_invest:
            to_invest -= to_donate
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            donation.close_date = datetime.now()
            session.add(donation)
            continue
        if to_donate == to_invest:
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            donation.close_date = datetime.now()
            charity_project.invested_amount = charity_project.full_amount
            charity_project.fully_invested = True
            charity_project.close_date = datetime.now()
            session.add(donation)
            session.add(charity_project)
            to_invest = 0
            break
        if to_donate > to_invest:
            charity_project.invested_amount = charity_project.full_amount
            charity_project.fully_invested = True
            charity_project.close_date = datetime.now()
            donation.invested_amount += to_invest
            session.add(charity_project)
            session.add(donation)
            to_invest = 0
            break
    if to_invest != 0:
        charity_project.invested_amount = (
                charity_project.full_amount - to_invest
        )
        session.add(charity_project)
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


