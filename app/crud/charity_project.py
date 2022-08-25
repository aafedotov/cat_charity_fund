from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Получение проекта по id."""
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        project_id = project_id.scalars().first()
        return project_id

    async def get_projects_to_invest(
            self,
            session: AsyncSession
    ) -> list[CharityProject]:
        """Получение незакрытых проектов."""

        free_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == false()
            ).order_by(CharityProject.create_date)
        )
        return free_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
