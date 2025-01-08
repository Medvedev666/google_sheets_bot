import logging
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv("SECRET_KEY"))
DATABASE_NAME = str(os.getenv("DATABASE_NAME"))



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Credentials for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = str(os.getenv("SERVICE_ACCOUNT_FILE"))

RANGE_LIST = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',	'y', 'z'
]

ADMIN_LIST = os.getenv("ADMIN_LIST")
logger.info(f'{ADMIN_LIST=}')
SPREADSHEET_ID = str(os.getenv("SPREADSHEET_ID"))