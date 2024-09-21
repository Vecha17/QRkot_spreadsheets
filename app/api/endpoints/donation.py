from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationGetAll
from app.services.invest import donation_process

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationGetAll],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def get_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_by_user(user.id, session)


@router.post(
    '/',
    response_model=DonationDB,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donation_ = await donation_crud.create(
        donation, session, user, commit_flag=False
    )
    sources = await charity_project_crud.get_uninvested(session)
    new_sources = donation_process(donation_, sources)
    await session.commit()
    await session.refresh(donation_)
    [await session.refresh(new_source) for new_source in new_sources]
    return donation_
