from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get_charity_project_by_name(
        room_name, session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_fully_invest(
        charity_project_id: int,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нельзя изменять/удалять полностью проинвестированый проект!'
            )
        )


def check_before_edit(
        obj_in,
        invested_amount
) -> None:
    for key, value in obj_in:
        if key == 'full_amount' and value:
            if value < invested_amount:
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=(
                        'Запрещено устанавливать требуемую'
                        'сумму меньше внесённой!'
                    )
                )
        if key == 'description' and value is not None:
            if value == '':
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail='Проект должен содержать описание!'
                )
        if key == 'name' and value is not None:
            if value == '':
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail='Проект должен содержать имя!'
                )


async def check_before_delete(
        charity_project_id: int,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалять проинвестированый проект!'
        )
