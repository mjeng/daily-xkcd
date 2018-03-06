import time
import sys
import random
import schedule
from pathlib import Path

from utils import *

PROJECT_PATH = ""

def execute_task(user_file, client, send_to):
    f = open(user_file, 'r')
    comics_left = list(f.readlines())
    f.close()

    if comics_left == []:
        sys.exit("sent every available comic :O")

    comic_choice = random.choice(comics_left)
    comics_left.remove(comic_choice)
    comic_num = int(comic_choice)

    # write updated list back to file
    f = open(user_file, 'w')
    for comic in comics_left:
        f.write(comic)
    f.close()

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
    user_file = PROJECT_PATH + str(send_to) + ".txt"
    path_obj = Path(user_file)
    file_exists = path_obj.is_file()

    # so that we can stop program and restart where we left off
    if file_exists:
        pass
    else:
        f = open(user_file, 'w+')
        for i in range(num_existing_comics):
            f.write(str(i+1) + "\n")
        f.close()

    schedule_cmd = "schedule.every(" + str(frq['num']) + ")." + frq['units'] + ".do(execute_task, user_file, client, send_to)"
    exec(schedule_cmd)

    try:
        while True:
            # when new comics are added, they'll be automatically added to text file of unused comics
            old_num_existing = num_existing_comics
            num_existing_comics = most_recent_comic_num()
            if num_existing_comics - old_num_existing != 0:
                f = open(user_file, 'a')
                for i in range(num_existing_comics - old_num_existing):
                    f.write(str(num_existing_comics - i) + "\n")
                f.close()

            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit("\nExiting program\n")
