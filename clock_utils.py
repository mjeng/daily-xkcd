import datetime

###############################################
UTC_TO_PST = -7
###############################################

def round_halfhr(min):
    closest = round(min / 30)
    if closest == 0:
        return '00'
    elif closest == 1:
        return '30'
    else:
        raise AssertionError("Somehow, rounded number wasn't 0 or 1")

def get_time():
    utcnow = datetime.datetime.utcnow()
    hour = utcnow.hour
    min = utcnow.minute
    pst_hour = (hour + UTC_TO_PST) % 24
    pst_hour_str = str(pst_hour).zfill(2)
    rounded_min_str = round_halfhr(min)
    timestr = pst_hour_str + rounded_min_str
    return timestr
