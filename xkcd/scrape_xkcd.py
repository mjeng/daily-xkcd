import time
import sys
import random
import schedule

from xkcd.utils import *

# TODO write list of unused comics to text file

def execute_task(unused_comics, client, send_to):
    comic_num = random.choice(unused_comics)
    unused_comics.remove(comic_num)

    if unused_comics == []:
        sys.exit("wtf this program has been running for too long")

    img_url = find_comic(comic_num)
    img_caption = find_comic_caption(comic_num)

    if img_url is None:
        print("Could not find comic #" + str(comic_num))
    else:
        print("Sending comic: " + str(comic_num))
        if img_caption is None:
            client.send_mms(send_to, img_url)
        else:
            client.send_mms(send_to, img_url, img_caption)


def main(client, send_to, frq):
    num_existing_comics = most_recent_comic_num()
    unused_comics = [i+1 for i in range(num_existing_comics)]

    schedule_cmd = "schedule.every(" + str(frq['num']) + ")." + frq['units'] + ".do(execute_task, unused_comics, client, send_to)"
    exec(schedule_cmd)

    try:
        while True:
            # when new comics are added, they'll be automatically added to list of unused comics
            old_num_existing = num_existing_comics
            num_existing_comics = most_recent_comic_num()
            for i in range(num_existing_comics - old_num_existing):
                unused_comics.append(num_existing_comics - i)

            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit("\nExiting program\n")
