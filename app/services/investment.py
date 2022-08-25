from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import CharityProjectDB
from app.schemas.donation import DonationDB


async def donation_processing(
        donation_id: int,
        session: AsyncSession
) -> DonationDB:
    """Процессинг инвестиций при добавлении нового доната."""

    free_projects = await charity_project_crud.get_projects_to_invest(session)
    donation = await donation_crud.get(donation_id, session)
    to_donate = donation.full_amount
    for project in free_projects:
        to_invest = project.full_amount - project.invested_amount
        if to_donate < to_invest:
            project.invested_amount += to_donate
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            donation.close_date = datetime.now()
            to_donate = 0
            session.add(project)
            session.add(donation)
            break
        if to_donate == to_invest:
            project.invested_amount = project.full_amount
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            project.fully_invested = True
            donation.close_date = datetime.now()
            project.close_date = datetime.now()
            to_donate = 0
            session.add(project)
            session.add(donation)
            break
        if to_donate > to_invest:
            to_donate -= to_invest
            project.invested_amount = project.full_amount
            project.fully_invested = True
            project.close_date = datetime.now()
            session.add(project)
    if to_donate != 0:
        donation.invested_amount = donation.full_amount - to_donate
        session.add(donation)
    await session.commit()
    await session.refresh(donation)
    return donation


async def project_processing(
        project_id: int,
        session: AsyncSession
) -> CharityProjectDB:
    """Процессинг инвестиций при додавлении или изменении проектов."""

    charity_project = await charity_project_crud.get(project_id, session)
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
