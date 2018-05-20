import sys
from time import strftime, gmtime
import numpy as np
import client
from client import WORKBOOK_NAME

def get_time():
    TIME_FORMAT = "%Y-%M-%d %H:%M:%S"
    return strftime(TIME_FORMAT, gmtime())

STAT_START_COL = {"letter": 'G', "number": 7}
AUTHOR = "Matthew Jeng"
TIMEZONE = "UTC"
COLUMNS = "name, number, num comics drawn, comics-seen (up to half), comics-left (after half)"

METADATA = {"author": AUTHOR,
            "timezone": TIMEZONE,
            "ss-init time": None, # initialize later
            "num users": "=sum({1}:{1})", # format later
            "comics sent": "=sum({2}:{2})", # format later
            "columns": COLUMNS}

def initialize_metadata():
    METADATA["ss-init time"] = get_time()
    c = STAT_START_COL
    letters = [c, chr(ord(c["letter"]) + 1), chr(ord(c["letter"]) + 2)]
    METADATA["num users"] = METADATA["num users"].format(*letters)
    METADATA["comics sent"] = METADATA["comics sent"].format(*letters)

def get_shaped_range(ws, r):
    dim = (r[2]-r[0]+1, r[3]-r[1]+1)
    arr = np.array(ws.range(*r)).reshape(*dim)
    return [list(a) for a in arr]


def run_setup():
    try:
        wbs = client.CLIENT.openall()
        assert len(wbs) == 0, "Workbooks already exist"
    except AssertionError as e:
        print(e)
        print(wbs)

    # NOTE it's possible to create multiple workbooks of the same name (not same of worksheets)
    # TODO change back the client.CLIENT.create()
    wb = client.CLIENT.open(WORKBOOK_NAME)

    # # retrieve workbook
    # try:
    #     wb = client.CLIENT.open(WORKBOOK_NAME)
    # except gspread.exceptions.SpreadsheetNotFound:
    #     # TODO report error somehow when server is setup


    # CREATE SHEETS
    # metadata sheet
    ws1 = wb.sheet1
    ws1.update_title("metadata")

    MD_RANGE = (1, 1, len(METADATA), 2)
    md_cells = get_shaped_range(ws1, MD_RANGE)

    initialize_metadata()
    md_items = list(METADATA.items())
    assert len(md_cells) == len(md_items), "Metadata dimensions off"
    for i in range(len(md_cells)):
        md_cells[i][0].value = md_items[i][0]
        md_cells[i][1].value = md_items[i][1]
    ws1.update_cells(sum(md_cells, []), "USER_ENTERED")

    ###

    N = STAT_START_COL["number"]
    C = STAT_START_COL["letter"]

    stathead_cells = ws1.range(1,N, 1,N+2)
    stathead_cells[0].value = "ws"
    stathead_cells[1].value = "user count"
    stathead_cells[2].value = "comics sent"
    ws1.update_cells(stathead_cells)

    ###

    SHEETNAME_FORMAT = "{0}:00-{0}:59"
    # data sheets
    # NOTE I put this in front of last metadata section because google sheets
    #   needs the sheets created before referencing - references don't automatically
    #   update
    DIMENSIONS = (1, 5)
    for i in range(24):
        wb.add_worksheet(SHEETNAME_FORMAT.format(i), *DIMENSIONS)

    ###

    USERCOUNT_FORMAT = '=COUNTA(INDIRECT(' + C + '{0}&"!A:A"))'
    COMICSSENT_FORMAT = '=SUM(INDIRECT(' + C + '{0}&"!C:C"))'
    stat_cells_range = (2,N, 25,N+2)
    stat_cells = get_shaped_range(ws1, stat_cells_range)
    for i in range(len(stat_cells)):
        stat_cells[i][0].value = SHEETNAME_FORMAT.format(i)
        stat_cells[i][1].value = USERCOUNT_FORMAT.format(i+2)
        stat_cells[i][2].value = COMICSSENT_FORMAT.format(i+2)
    ws1.update_cells(sum(stat_cells, []), "USER_ENTERED")


# NOTE only run during testing phase
def reset():
    wb = client.CLIENT.open(WORKBOOK_NAME)
    wss = wb.worksheets()[1:]
    for ws in wss:
        wb.del_worksheet(ws)
    wb.sheet1.clear()

# NOTE Doesn't run if not specifically running setup - file should only be run once.
#      If imported and not specifically run, name will be "setup" not "__main__"
if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == "--run" or arg == "-r":
        run_setup()
    elif arg == "--clean" or arg == "-c":
        reset()

# TODO move this somewhere useful
# try:
#     # in the case that credentials expire
#     wb.sheet1
# except gspread.exceptions.APIError as e:
#     # TODO replace with console reporting
#     # TODO refresh credentials
#     print(e)
