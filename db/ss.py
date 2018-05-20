import client
from client import WORKBOOK_NAME

# Find a workbook by name
wb = client.CLIENT.open(WORKBOOK_NAME)
ws1 = wb.sheet1

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
