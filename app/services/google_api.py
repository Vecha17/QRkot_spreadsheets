from datetime import datetime as dt

from aiogoogle import Aiogoogle
from dateutil import parser

from app.core import conts
from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'

SPREADSHEETS_BODY = dict(
    properties=dict(
        title=f'Отчет от {dt.now().strftime(FORMAT)}',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=100,
            columnCount=3,
        )
    ))]
)
TABLE_VALUES = [
    ['Отчёт от', 'time'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> tuple[str, str]:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADSHEETS_BODY
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    spreadsheets_url = response['spreadsheetUrl']
    return spreadsheet_id, spreadsheets_url


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = str(dt.now().strftime(FORMAT))
    TABLE_VALUES[0][1] = now_date_time
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *TABLE_VALUES,
        *[list(map(str, (
            project.name,
            (
                parser.parse(str(project.close_date)) -
                parser.parse(str(project.create_date))
            ),
            project.description))
        ) for project in charity_projects]
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    if len(table_values) > conts.ROW_COUNT:
        raise Exception('Передаваемые данные не помещаются в таблицу!')
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:100',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
