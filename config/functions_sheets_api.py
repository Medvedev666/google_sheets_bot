from googleapiclient.discovery import build
from google.oauth2 import service_account

from config.config import SERVICE_ACCOUNT_FILE, SCOPES, logger, SPREADSHEET_ID



# Авторизация
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Создание сервиса
service = build('sheets', 'v4', credentials=credentials)


def handle_data_for_google_spreadsheet(values):

    request = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="A2",
        valueInputOption="RAW",
        body={'values': [values]}
    )
    response = request.execute()

    logger.info(f"Данные успешно добавлены: {response}")
    return response




def get_number_from_google_spreadsheet():

    # Запрос данных с листа "работники"
    range_ = "работники!A2:D"  # Указываем диапазон, где лежат данные (можно изменить, если нужно больше столбцов)
    request = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_
    )

    # Выполнение запроса
    response = request.execute()

    result = []

    # Проверка, есть ли данные в ответе
    if 'values' in response:
        data = response['values']
        for row in data:
            print(row)
            try:
                if row and row[0] and row[1]  and row[2] and row[3]:
                    print(row)  # Вывод каждой строки данных
                    result.append([row[0], row[1], row[2], row[3]])
            except:
                pass
    else:
        logger.warning("Данные не найдены на листе 'работники'.")

    return result

