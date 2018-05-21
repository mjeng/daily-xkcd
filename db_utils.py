import db_client
from db_client import WORKBOOK_NAME

MRCN_CELL = "B6"

def update_mrcn(new_mrcn):

    assert type(new_mrcn) == int, "new_mrcn not of type int; has value {0}".format(new_mrcn)
    ws1 = db_client.WB.sheet1
    curr_mrcn = int(ws1.acell(MRCN_CELL).numeric_value())

    if curr_mrcn != new_mrcn:
        ws1.update_acell(MRCN_CELL, new_mrcn)
