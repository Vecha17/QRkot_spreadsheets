from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject

from .base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

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
