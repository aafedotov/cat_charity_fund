from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.crud.base import CRUDBase
from app.models import User
from app.models.donation import Donation


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User,
    ) -> list[Donation]:
        """Получение донатов конкретного пользователя."""

        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            ).order_by(Donation.create_date)
        )
        return donations.scalars().all()

    async def get_free_donations(
            self,
            session: AsyncSession
    ) -> list[Donation]:
        """Получение списка нераспределенных донатов."""

        donations = await session.execute(
            select(Donation).where(
                Donation.fully_invested == false()
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
