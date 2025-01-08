from googleapiclient.discovery import build
from google.oauth2 import service_account

from config.config import SERVICE_ACCOUNT_FILE, SCOPES, logger, SPREADSHEET_ID




def handle_data_for_google_spreadsheet(values):
    
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('sheets', 'v4', credentials=credentials)

    request = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="A2",
        valueInputOption="RAW",
        body={'values': [values]}
    )
    response = request.execute()

    logger.info(f"Данные успешно добавлены: {response}")
    return response


