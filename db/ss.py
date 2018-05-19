# cell limit in workbook is 2,000,000

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name
ss = client.open("daily-xkcd user info")
sheet = ss.sheet1

# i = 0
# for ws in wss:
#     i += 1
#     try:
#         print(i)
#         ss.del_worksheet(ws)
#     except gspread.exceptions.APIError:
#         time.sleep(10)
#
#
# def insert_row(sheet, row):
#     sheet.append_row(row)

# try:
#     for i in range(200):
#         contents = ["bloop"] * 20
#         sheet.append_row([i] + contents)
# except gspread.exceptions.APIError:
#     print("blep")
