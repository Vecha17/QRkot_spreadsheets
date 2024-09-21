from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject

from .base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession
    ):
        charity_project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == charity_project_name
            )
        )
        charity_project = charity_project.scalars().first()
        return charity_project

    async def get_closet_charity_projects(
        self,
        session: AsyncSession
    ):
        charity_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(
                (extract('epoch', CharityProject.close_date)) -
                (extract('epoch', CharityProject.create_date))
            )
        )
        charity_projects = charity_projects.scalars().all()
        return charity_projects


charity_project_crud = CRUDCharityProject(CharityProject)
