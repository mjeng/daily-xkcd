import os, json
import gspread
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

def setup_db():
    global wb
    print(os.environ)
    _service_account_info = json.loads(os.environ["GOOGLE_AUTH"])
    print(os.environ["GOOGLE_AUTH"])
    print("\n\n\n\n")
    print(_service_account_info)
    _scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    _credentials = service_account.Credentials.from_service_account_info(_service_account_info)
    _scoped_credentials = _credentials.with_scopes(_scope)
    _spreadsheetId = os.environ["WB_ID"]
    _gc = gspread.Client(auth=_scoped_credentials)
    _gc.session = AuthorizedSession(_scoped_credentials)
    wb = _gc.open_by_key(_spreadsheetId)

setup_db()
