from datetime import datetime
from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.schemas.charity_project import CharityProjectDB
from app.services.google_api import (
    spreadsheets_create, set_user_permissions, spreadsheets_update_value
)
from app.crud.charity_project import charity_project_crud
router = APIRouter()


@router.post(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    charity_projects = await charity_project_crud.get_closet_charity_projects(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid, charity_projects, wrapper_services
    )
    return charity_projects
