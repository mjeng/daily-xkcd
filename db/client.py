# cell limit in workbook is 2,000,000
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
_SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

_CREDS = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', _SCOPE)
client = gspread.authorize(_CREDS)

WORKBOOK_NAME = "daily-xkcd user info"
