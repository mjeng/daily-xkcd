import os
import twilio_utils, scrape_utils, db_utils
import random

# TODO: temporary; replace with heroku config
f = open("private.txt", 'r')
account_sid = f.readline()[:-1] # to get rid of \n
auth_token = f.readline()[:-1]
send_to = f.readline()[:-1]
send_from = f.readline()[:-1]
f.close()

def add_db_entry(name, number, timestr):
    db_utils.add_entry(name, number, timestr)

def run_once(name, number):

    mrcn = scrape_utils.most_recent_comic_num()
    comic_num = random.randint(1, mrcn)

    mms = twilio_utils.MMS(name, number, comic_num)

    comic_url = scrape_utils.find_comic_url(comic_num)
    caption = scrape_utils.find_comic_caption(comic_num)

    mms.update(comic_url, caption)

    twilio_client = twilio_utils.ClientWrapper(account_sid, auth_token, send_from)
    twilio_client.send_mms(mms)


# NOTE: runs periodically vis-a-vis heroku scheduler
def run():

    # TODO: retrieve most_recent_comic_num
    mrcn = scrape_utils.most_recent_comic_num()
    # TODO: send to db, update if necessary
    db_utils.update_mrcn(mrcn)

    # TODO: request users at certain time slot; db should automatically update here
    #       should receive a list of MMS objects with name, phone #, comic #, (empty) caption

    # TODO: call scraper and replace all comic #s with comic url and add in caption

    # TODO: call twilio and send all comics to phone # with greeting + caption
    twilio_client = twilio_utils.ClientWrapper(account_sid, auth_token, send_from)


# if __name__ == "__main__":
#     run()
