# cell limit in workbook is 2,000,000
import gspread
from oauth2client.service_account import ServiceAccountCredentials

_index = -__file__[::-1].find("/")
if _index > 0:
    _relpath = ""
else:
    _relpath = __file__[:_index]

# use creds to create a client to interact with the Google Drive API
_SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# TODO: change to config var
_CREDS = ServiceAccountCredentials.from_json_keyfile_name(_relpath + "client_secret.json", _SCOPE)
CLIENT = gspread.authorize(_CREDS)

WORKBOOK_NAME = "daily-xkcd user info"

# NOTE: It's possible to create multiple workbooks of the same name (not same of worksheets)
# retrieve workbook
try:
    WB = CLIENT.open(WORKBOOK_NAME)
except gspread.exceptions.SpreadsheetNotFound as e:
    # TODO: report error
    print(e)
    print("workbook doesn't exist??")

# in class authentication times out
def reload_client():
    global CLIENT, WB
    CLIENT = gspread.authorize(_CREDS)
    WB = CLIENT.open(WORKBOOK_NAME)
