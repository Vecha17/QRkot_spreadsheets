from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_before_delete, check_before_edit,
    check_charity_project_exists,
    check_fully_invest, check_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.invest import donation_process

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_progects(
    session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    charity_project = await charity_project_crud.create(
        charity_project, session, commit_flag=False
    )
    new_sources = donation_process(
        charity_project,
        await donation_crud.get_uninvested(session)
    )
    session.add_all(new_sources)
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_fully_invest(charity_project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    check_before_edit(obj_in, charity_project.invested_amount)
    return await charity_project_crud.update(
        charity_project, obj_in, session
    )


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_fully_invest(charity_project_id, session)
    await check_before_delete(charity_project_id, session)
    return await charity_project_crud.remove(
        charity_project, session
    )
