import logging
from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import (DRIVE_SERVICE_NAME, DRIVE_SERVICE_VERSION,
                             DRIVE_USER_PERMISSION_ROLE,
                             DRIVE_USER_PERMISSION_TYPE, MAJOR_DIMENSION_TYPE, PROJECT_DESCRIPTION_FIELD, PROJECT_NAME_FIELD, PROJECT_TIMEDIFF_FIELD,
                             SP_PROJECT_DESCRIPTION_COLUMN, SP_PROJECT_NAME_COLUMN,
                             SP_PROJECT_TIMEDIFF_COLUMN, SP_UPDATE_RANGE,
                             SP_UPDATE_VALUE_INPUT_OPTION,
                             SPREADSHEET_COLUMN_COUNT,
                             SPREADSHEET_CREATED_SUCEED,
                             SPREADSHEET_DATE_FORMAT, SPREADSHEET_DESCRIPTION,
                             SPREADSHEET_HEAD_TITLE, SPREADSHEET_ID,
                             SPREADSHEET_LOCALE, SPREADSHEET_MAIN_URL,
                             SPREADSHEET_ROW_COUNT, SPREADSHEET_SERVICE_NAME,
                             SPREADSHEET_SERVICE_VERSION,
                             SPREADSHEET_SHEETTYPE, SPREADSHEET_TITLE,
                             settings)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Функция для создания документа с таблицами"""
    now_date_time = datetime.now().strftime(SPREADSHEET_DATE_FORMAT)
    service = await wrapper_services.discover(
        SPREADSHEET_SERVICE_NAME,
        SPREADSHEET_SERVICE_VERSION
    )
    spreadsheet_body = {
        'properties': {'title': f'{SPREADSHEET_HEAD_TITLE} {now_date_time}',
                       'locale': SPREADSHEET_LOCALE},
        'sheets': [{'properties': {'sheetType': SPREADSHEET_SHEETTYPE,
                                   'sheetId': SPREADSHEET_ID,
                                   'title': SPREADSHEET_TITLE,
                                   'gridProperties': {'rowCount': SPREADSHEET_ROW_COUNT,
                                                      'columnCount': SPREADSHEET_COLUMN_COUNT}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    logging.info(f'{SPREADSHEET_CREATED_SUCEED} {SPREADSHEET_MAIN_URL}{spreadsheetid}')
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Функция для предоставления прав доступа
    вашему личному аккаунту к созданному документу"""
    permissions_body = {'type': DRIVE_USER_PERMISSION_TYPE,
                        'role': DRIVE_USER_PERMISSION_ROLE,
                        'emailAddress': settings.email}
    service = await wrapper_services.discover(
        DRIVE_SERVICE_NAME,
        DRIVE_SERVICE_VERSION
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        closed_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Функция записывает полученную из БД информацию в документ с таблицами"""
    now_date_time = datetime.now().strftime(SPREADSHEET_DATE_FORMAT)
    service = await wrapper_services.discover(
        SPREADSHEET_SERVICE_NAME,
        SPREADSHEET_SERVICE_VERSION
    )
    table_values = [
        [SPREADSHEET_HEAD_TITLE, now_date_time],
        [SPREADSHEET_DESCRIPTION],
        [SP_PROJECT_NAME_COLUMN, SP_PROJECT_TIMEDIFF_COLUMN, SP_PROJECT_DESCRIPTION_COLUMN]
    ]
    for project in closed_projects:
        new_row = [str(project[PROJECT_NAME_FIELD]), str(timedelta(seconds=project[PROJECT_TIMEDIFF_FIELD])), str(project[PROJECT_DESCRIPTION_FIELD])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': MAJOR_DIMENSION_TYPE,
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=SP_UPDATE_RANGE,
            valueInputOption=SP_UPDATE_VALUE_INPUT_OPTION,
            json=update_body
        )
    )
