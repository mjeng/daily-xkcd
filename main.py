import sender
import scrape_xkcd


# NOTE: runs periodically vis-a-vis heroku scheduler
def run():
    # TODO: retrieve most_recent_comic_num

    # TODO: send to db, update if necessary

    # TODO: request users at certain time slot; db should automatically update here
    #   should receive a list of MMS objects with name, phone #, comic #, (empty) caption

    # TODO: call scraper and replace all comic #s with comic url and add in caption

    # TODO: call twilio and send all comics to phone # with greeting + caption


if __name__ == "__main__":
    run()
