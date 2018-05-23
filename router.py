import os
import twilio_utils, scrape_utils, db_utils, server_utils
import random


###############################################
CONFIRMATION_FORMAT = "Hey {0}! This text is just to confirm that you've subscribed " \
    + "to getting daily texts at {1} PST every day from daily-xkcd. You can always reply " \
    + "STOP if you don't want to receive messages anymore!"

def twilio_setup():
    global twilio_client
    SID = os.environ["TWILIO_SID"]
    TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
    NUMBER = os.environ["TWILIO_NUMBER"]

    twilio_client = twilio_utils.ClientWrapper(SID, TOKEN, NUMBER)

twilio_setup()
###############################################


def add_db_entry(name, number, timestr):
    # the number should already be validated by the server-side checks
    pnc = twilio_client.client.lookups.phone_numbers(number)
    pni = pnc.fetch()
    pn = pni.phone_number

    db_utils.add_entry(name, pn, timestr)


def send_sub_confirmation(name, number, time):

    sms = twilio_utils.SMS(number, CONFIRMATION_FORMAT.format(name, time))

    twilio_client.send_sms(sms)


def run_once(name, number):

    mrcn = scrape_utils.most_recent_comic_num()
    comic_num = random.randint(1, mrcn)

    mms = twilio_utils.MMS(name, number, comic_num)

    comic_url = scrape_utils.find_comic_url(comic_num)
    caption = scrape_utils.find_comic_caption(comic_num)

    mms.update(comic_url, caption)

    twilio_client.send_mms(mms)


# called periodically by clock dyno
def run(timestr):

    server_utils.log("RUNNING with timestr " + timestr)

    # Retrieve most_recent_comic_num
    mrcn = scrape_utils.most_recent_comic_num()

    # Send to db, update if necessary
    db_utils.update_mrcn(mrcn)

    # Request users at certain time slot; db should automatically update here
    # Should receive a list of MMS objects with name, phone #, comic #, (empty) caption
    mms_list = db_utils.retrieve_mms_list(timestr)

    # Call scraper and replace all comic #s with comic url and add in caption
    for mms in mms_list:
        # If one mms update errors, the others should still send
        try:
            comic_num = mms.comic_num
            comic_url = scrape_utils.find_comic_url(comic_num)
            comic_caption = scrape_utils.find_comic_caption(comic_num)
            mms.update(comic_url, comic_caption)
        except Exception as e:
            server_utils.log(e)
            continue

    # Call twilio and send all comics to phone # with greeting + caption
    for mms in mms_list:
        # If one message sent errors, the others should still send
        try:
            twilio_client.send_mms(mms)
        except Exception as e:
            server_utils.log(e)
            continue
