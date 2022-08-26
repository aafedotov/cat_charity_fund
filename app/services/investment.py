from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import CharityProjectDB
from app.schemas.donation import DonationDB


def close_invest(obj: Union[CharityProjectDB, DonationDB]) -> None:
    """Закрытие проекта/доната."""
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def investment_processing(
        session: AsyncSession
) -> None:
    """Процессинг инвестиций."""
    free_projects = await charity_project_crud.get_projects_to_invest(session)
    free_donations = await donation_crud.get_free_donations(session)
    if not free_donations and not free_projects:
        return
    for donation in free_donations:
        for project in free_projects:
            to_invest = project.full_amount - project.invested_amount
            to_donate = donation.full_amount - donation.invested_amount
            diff = to_invest - to_donate
            if diff == 0:
                close_invest(donation)
                close_invest(project)
            if diff < 0:
                donation.invested_amount += abs(diff)
                close_invest(project)
            if diff > 0:
                project.invested_amount += to_donate
                close_invest(donation)

    await session.commit()
