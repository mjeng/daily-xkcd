import os
import twilio_utils, scrape_utils, db_utils
import random

def add_db_entry(name, number, timestr):
    db_utils.add_entry(name, number, timestr)

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
