# NOTE: run with one of the following:
#   python3 db_setup.py --run
#   python3 db_setup.py --clean

import sys
from time import strftime, gmtime
import numpy as np
import db_client
import scrape_utils

STAT_START_COL = {"letter": 'E', "number": 5}
AUTHOR = "Matthew Jeng"
TIMEZONE = "UTC"
COLUMNS = ["Name", "Phone #", "# Comics Sent", "Comics Sent"]
BLANK = ''

METADATA = {"author": AUTHOR,
            "timezone": TIMEZONE,
            "ss-init time": None, # initialize later
            "num users": "=sum({1}:{1})", # format later
            "comics sent": "=sum({2}:{2})", # format later
            "MRCN": None, # initialize later
            BLANK: BLANK,
            "sms price": "$0.0075",
            "mms price": "$0.02"}


def get_time():
    TIME_FORMAT = "%Y-%M-%d %H:%M:%S"
    return strftime(TIME_FORMAT, gmtime())

def initialize_metadata():
    METADATA["ss-init time"] = get_time()
    c = STAT_START_COL
    letters = [c, chr(ord(c["letter"]) + 1), chr(ord(c["letter"]) + 2)]
    METADATA["num users"] = METADATA["num users"].format(*letters)
    METADATA["comics sent"] = METADATA["comics sent"].format(*letters)
    METADATA["MRCN"] = scrape_utils.most_recent_comic_num()

def get_shaped_range(ws, r):
    dim = (r[2]-r[0]+1, r[3]-r[1]+1)
    arr = np.array(ws.range(*r)).reshape(*dim)
    return [list(a) for a in arr]

def run_setup():

    # CREATE SHEETS
    # metadata sheet
    ws = db_client.WB.sheet1
    ws.update_title("metadata")

    MD_RANGE = (1, 1, len(METADATA), 2)
    md_cells = get_shaped_range(ws, MD_RANGE)

    initialize_metadata()
    md_items = list(METADATA.items())
    assert len(md_cells) == len(md_items), "Metadata dimensions off"
    for i in range(len(md_cells)):
        md_cells[i][0].value = md_items[i][0]
        md_cells[i][1].value = md_items[i][1]
    ws.update_cells(sum(md_cells, []), "USER_ENTERED")

    ###

    N = STAT_START_COL["number"]
    C = STAT_START_COL["letter"]

    stathead_cells = ws.range(1,N, 1,N+2)
    stathead_cells[0].value = "ws"
    stathead_cells[1].value = "user count"
    stathead_cells[2].value = "comics sent"
    ws.update_cells(stathead_cells)

    ###

    ########
    # data sheets

    # NOTE I put this in front of last metadata section because google sheets needs
    #   the sheets created before referencing - references don't automatically update
    SHEETNAME_FORMAT = "T-{0}{1}"
    DIMENSIONS = (1, 4)
    sheet_names = []
    for i in range(24):
        sn1 = SHEETNAME_FORMAT.format(str(i).zfill(2), '00')
        sn2 = SHEETNAME_FORMAT.format(str(i).zfill(2), '30')
        ws1 = db_client.WB.add_worksheet(sn1, *DIMENSIONS)
        ws1.append_row(COLUMNS)
        ws2 = db_client.WB.add_worksheet(sn2, *DIMENSIONS)
        ws2.append_row(COLUMNS)
        sheet_names.extend([sn1, sn2])
    ########

    ###

    USERCOUNT_FORMAT = '=COUNTA(INDIRECT(' + C + '{0}&"!A:A")) - 1'
    COMICSSENT_FORMAT = '=SUM(INDIRECT(' + C + '{0}&"!C:C"))'
    START_ROW = 2
    stat_cells_range = (START_ROW,N, START_ROW+len(sheet_names),N+2)
    stat_cells = get_shaped_range(ws, stat_cells_range)
    for i in range(len(sheet_names)):
        stat_cells[i][0].value = sheet_names[i]
        stat_cells[i][1].value = USERCOUNT_FORMAT.format(i+2)
        stat_cells[i][2].value = COMICSSENT_FORMAT.format(i+2)
    ws.update_cells(sum(stat_cells, []), "USER_ENTERED")


def reset():
    wb = db_client.WB
    wss = wb.worksheets()[1:]
    for ws in wss:
        wb.del_worksheet(ws)
    wb.sheet1.clear()

# NOTE: Doesn't run if not specifically running setup - file should only be run once.
#       If imported, name will not be "__main__".
if __name__ == "__main__":
    try:
        arg = sys.argv[1]
        if arg == "--run" or arg == "-r":
            run_setup()
        elif arg == "--clean" or arg == "-c":
            reset()
        else:
            print("Please use tags --run [-r] or --clean [-c]")
    except IndexError as e:
        print("IndexError: No argument given")
