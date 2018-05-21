import re

###############################################
TRY = "try it"
SUB = "submit"

TIME_FORMAT = "^[0-9]{2}:[0-9]{2} [AP]M"
HOURS = [str(i+1).zfill(2) for i in range(12)]
MINUTES = ['00', '30']
AM = 'AM'
PM = 'PM'
###############################################

# NOTE: turns out you can change the values of the select box before submission
#   so validating to make sure it's one of the options provided
def parse_validate_time(time):
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

    res = re.findall(TIME_FORMAT, time)
    assert len(res) == 1, "Issue with time format"

    hours = res[0:2]
    minutes = res[3:5]
    ampm = res[6:8]

    assert hours in HOURS, "Corrupted input"
    assert minutes in MINUTES, "Corrupted input"
    assert ampm in [AM, PM], "Corrupted input"

    if ampm == AM and hours == '12':
        hours = '00'
    if ampm == PM and hours != '12':
        hours = str(int(hours) + 12)

    return hours + minutes
