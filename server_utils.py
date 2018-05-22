import re
import twilio.base.exceptions

###############################################
TRY = "try it"
SUB = "submit"

TIME_FORMAT = "^[0-9]{2}:[0-9]{2} [AP]M"
FORMAT_LENGTH = 8
HOURS = [str(i+1).zfill(2) for i in range(12)]
MINUTES = ['00', '30']
AM = 'AM'
PM = 'PM'

MAX_NAME_LENGTH = 100
NO_ERR = 0
NAME_ERR = 1
NUM_ERR = 2
TIME_ERR = 3
SUBMIT_ERR = 4
###############################################

# NOTE: turns out you can change the values of the select box before submission
#   so validating to make sure it's one of the options provided
def parse_time(time):
    """
    Returns string denoting the time with format 'hhmm'. Function makes sure the
    selected option is one of the provided ones.
    >>> parse_validate_time("12:30 AM")
    '0030'
    >>> parse_validate_time("6:30 PM")
    '1830'
    >>> parse_validate_time("6:31 PM")
    AssertionError
    """

    # NOTE: validation not necessary here anymore but just kept it ¯\_(ツ)_/¯

    res = re.findall(TIME_FORMAT, time.zfill(FORMAT_LENGTH))
    assert len(res) == 1, "Issue with time format"
    raw = res[0]

    hours = raw[0:2]
    minutes = raw[3:5]
    ampm = raw[6:8]

    assert hours in HOURS, "Corrupted input"
    assert minutes in MINUTES, "Corrupted input"
    assert ampm in [AM, PM], "Corrupted input"

    if ampm == AM and hours == '12':
        hours = '00'
    if ampm == PM and hours != '12':
        hours = str(int(hours) + 12)

    return hours + minutes

def validate_name(name):
    try:
        assert isinstance(name, str)
        assert len(name) <= MAX_NAME_LENGTH
    except AssertionError:
        return False
    return True

def validate_number(number, twilio_client):
    pnc = twilio_client.client.lookups.phone_numbers(number)
    try:
        pn = pnc.fetch()
        num = pn.phone_number
    except twilio.base.exceptions.TwilioRestException:
        return False
    return True

def validate_time(time):
    res = re.findall(TIME_FORMAT, time.zfill(FORMAT_LENGTH))
    try:
        assert len(res) == 1, "Issue with time format"
    except AssertionError:
        return False

    raw = res[0]
    hours = raw[0:2]
    minutes = raw[3:5]
    ampm = raw[6:8]

    try:
        assert hours in HOURS, "Corrupted input"
        assert minutes in MINUTES, "Corrupted input"
        assert ampm in [AM, PM], "Corrupted input"
    except AssertionError:
        return False
    return True

def validate_submit_type(submit_type):
    try:
        assert submit_type == TRY or submit_type == SUB
    except AssertionError:
        return False
    return True

def validate_inputs(name, number, twilio_client, time, submit_type):
    if not validate_name(name):
        return NAME_ERR
    if not validate_number(number, twilio_client):
        return NUM_ERR
    if not validate_time(time):
        return TIME_ERR
    if not validate_submit_type(submit_type):
        return SUBMIT_ERR
    return NO_ERR

# just to have something more official/readable
def report(str):
    print(str)
