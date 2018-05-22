import db_client
import twilio_utils
import numpy as np
import random


###############################################
METADATA = "metadata"
MRCN_CELL = "B6"
###############################################


############### HELPERS ###############
def time2sheet(timestr):
    return "T-" + timestr

def get_shaped_range(ws, r):
    dim = (r[2]-r[0]+1, r[3]-r[1]+1)
    arr = np.array(ws.range(*r)).reshape(*dim)
    return [list(a) for a in arr]

def flatten(cells):
    return sum(cells, [])

def make_list(csv):
    strlist = csv.split(',')
    rv = [int(s) for s in strlist]
    return rv

def make_csv(lst):
    rstr = ""
    for i in lst:
        rstr += str(i) + ','
    if lst != []:
        rstr = rstr[:-1]
    return rstr

def find_comic_num(mrcn, list_sent):
    found = False
    while not found:
        rnum = random.randint(1, mrcn)
        if rnum not in list_sent:
            found = True
    return rnum
#######################################


############### PRIMARY ###############
def update_mrcn(new_mrcn):

    assert type(new_mrcn) == int, "new_mrcn not of type int; has value {0}".format(new_mrcn)
    ws1 = db_client.wb.sheet1
    curr_mrcn = int(ws1.acell(MRCN_CELL).numeric_value())

    if curr_mrcn != new_mrcn:
        ws1.update_acell(MRCN_CELL, new_mrcn)


def retrieve_mms_list(timestr):
    sheet_name = time2sheet(timestr)
    wss = db_client.wb.worksheets()[1:] # First worksheet is metadata
    sheet_names = [ws.title for ws in wss]
    assert METADATA not in sheet_names, "Order of database sheets mixed up"
    assert sheet_name in sheet_names, "Invalid sheet_name"

    ws = db_client.wb.worksheet(sheet_name)
    if ws.get_all_values() == []:
        return []

    top_left = (1, 1)
    bot_right = (ws.row_count, ws.col_count)

    if ws.row_count == 1:
        cells = [ws.range(*top_left, *bot_right)]
    else:
        cells = get_shaped_range(ws, [*top_left, *bot_right])
    print("row count =", ws.row_count)
    print("cells\n", cells)

    mrcn = db_client.wb.sheet1.acell(MRCN_CELL)
    mms_list = []
    for i, row in enumerate(cells):
        name = row[0].value
        phone = row[1].value
        num_sent = row[2].value
        list_sent = make_list(row[3].value)

        print(list_sent)

        row[2].value += 1
        comic_num = find_comic_num(mrcn, list_sent)
        mms = twilio_utils.MMS(name, phone, comic_num)
        mms_list.append(mms)

        print(list_sent)
        list_sent.append(comic_num)
        row[3].value = make_csv(list_sent)
        print(row[3].value)

    cell_list = flatten(cells)
    ws.update_cells(cell_list)

    return mms_list
#######################################

############### SECONDARY ###############
def add_entry(name, number, timestr):
    sheet_name = time2sheet(timestr)
    ws = db_client.wb.worksheet(sheet_name)
    ws.append_row([name, number, 0, ''])
#########################################
