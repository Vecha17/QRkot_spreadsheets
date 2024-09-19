from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def add_object_in_session(obj, session):
    session.add(obj)
    await session.commit()
    await session.refresh(obj)


async def confirm_fully_invested(obj):
    setattr(
        obj,
        'fully_invested',
        True
    )
    setattr(
        obj,
        'close_date',
        datetime.now()
    )
    setattr(
        obj,
        'invested_amount',
        obj.full_amount
    )
    return obj


async def get_free_money(
        full_amount,
        session: AsyncSession,
):
    free_money = 0
    donation_obj = await session.execute(
        select(Donation).where(Donation.fully_invested == bool(False))
    )
    donation_obj = donation_obj.scalars().all()
    if donation_obj is not None:
        for donation in donation_obj:
            donat_full_amount = donation.full_amount
            donat_invested_amount = donation.invested_amount
            free_money += (
                donat_full_amount - donat_invested_amount
            )
            if free_money > full_amount:
                invested_amount = (
                    donat_full_amount -
                    (free_money - full_amount)
                )
                free_money = full_amount
                setattr(donation, 'invested_amount', invested_amount)
                break
            else:
                donation = await confirm_fully_invested(donation)
    return free_money


async def create_charity_project(
        charity_project,
        session: AsyncSession,
):
    full_amount = charity_project.full_amount
    free_money = await get_free_money(
        full_amount,
        session
    )

    if free_money == full_amount:
        charity_project = await confirm_fully_invested(charity_project)
    setattr(
        charity_project,
        'invested_amount',
        free_money
    )
    await add_object_in_session(
        charity_project, session
    )
    return charity_project


async def create_donation(
        donation,
        session: AsyncSession,
):
    charity_projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == bool(False)
        )
    )
    charity_projects = charity_projects.scalars().all()
    if charity_projects is not None:
        donation_invested_amount = 0
        free_money = donation.full_amount
        for charity_project in charity_projects:
            charity_project_full_amount = charity_project.full_amount
            charity_project_invested_amount = charity_project.invested_amount
            amount = (
                charity_project_full_amount -
                charity_project_invested_amount
            )
            if free_money > amount:
                donation_invested_amount = (
                    donation_invested_amount +
                    free_money - (free_money - amount)
                )
                charity_project = await confirm_fully_invested(charity_project)
                setattr(
                    donation,
                    'invested_amount',
                    donation_invested_amount
                )
                free_money -= amount
            elif free_money == amount:
                charity_project = await confirm_fully_invested(charity_project)
                donation = await confirm_fully_invested(donation)
                break
            else:
                charity_project_invested_amount = (
                    free_money + charity_project_invested_amount
                )
                setattr(
                    charity_project,
                    'invested_amount',
                    charity_project_invested_amount
                )
                donation = await confirm_fully_invested(donation)
                break
    await add_object_in_session(donation, session)
    return donation
