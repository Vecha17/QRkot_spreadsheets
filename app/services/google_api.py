import copy
from datetime import datetime as dt

from aiogoogle import Aiogoogle

from app.core import consts
from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'

SPREADSHEETS_BODY = dict(
    properties=dict(
        title='Отчет от',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=consts.SHEET_ID,
        title='Лист1',
        gridProperties=dict(
            rowCount=consts.ROW_COUNT,
            columnCount=consts.COLUMN_COUNT,
        )
    ))]
)
TABLE_VALUES = [
    ['Отчёт от', 'time'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> tuple[str, str]:
    now_date_time = dt.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = copy.deepcopy(SPREADSHEETS_BODY)
    spreadsheet_body['properties']['title'] = f'Отчёт от {now_date_time}'
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    table_values_hat = copy.deepcopy(TABLE_VALUES)
    table_values_hat[0][1] = str(dt.now().strftime(FORMAT))
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *table_values_hat,
        *[list(map(str, (
            project.name,
            (project.close_date - project.create_date),
            project.description))
        ) for project in charity_projects]
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    if len(table_values) > consts.ROW_COUNT:
        raise ValueError(
            f'Передаваемые данные не помещаются в таблицу! '
            f'{len(table_values)} > {consts.ROW_COUNT}'
        )
    for value in table_values:
        if len(value) > consts.COLUMN_COUNT:
            raise ValueError(
                f'Передаваемые данные не помещаются в таблицу! '
                f'{len(value)} > {consts.COLUMN_COUNT}'
            )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{len(table_values)}C{consts.COLUMN_COUNT}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
