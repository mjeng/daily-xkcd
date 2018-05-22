import os, json
import gspread
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

def setup_db():
    global wb
    # _service_account_info = json.load(open("client_secret.json"))
    # _spreadsheetId = '1WA3fo_5YPfwMVp9lVety6fiEn184iss2TeE_UAEqF6A'
    _service_account_info = json.loads(os.environ["GOOGLE_AUTH"])
    _spreadsheetId = os.environ["WB_ID"]
    _scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    _credentials = service_account.Credentials.from_service_account_info(_service_account_info)
    _scoped_credentials = _credentials.with_scopes(_scope)
    _gc = gspread.Client(auth=_scoped_credentials)
    _gc.session = AuthorizedSession(_scoped_credentials)
    wb = _gc.open_by_key(_spreadsheetId)

setup_db()
