from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import sys
import random
import schedule
import re

# TODO add xkcd's message to the text

def most_recent_comic_num():
    main_website = "https://xkcd.com/"
    page = urlopen(main_website)

    # Whole document
    soup = BeautifulSoup(page, 'html.parser')

    # Middle container containing comic and header/footer
    middle_container = soup.find("div", {"id": "middleContainer"})

    # Permanent link is located after an empty <br> tag
    # Finding <br> tag then taking next element
    perm_link = middle_container.find("br").next_sibling

    # Regex to get number out of perm_link
    regex_str = main_website + ".*/"
    match = re.search(regex_str, perm_link)
    comic_num = match.group(0)[len(main_website):][:-1]

    return int(comic_num)

ESCAPE_CHARACTERS = ['.', '*', '+', '?', '|']

def check_url(img_url):
    pattern = "https://imgs.xkcd.com/comics/"
    escaped_pattern = ''
    for c in pattern:
        if c in ESCAPE_CHARACTERS:
            escaped_pattern += "\\"
        escaped_pattern += c
    escaped_pattern += ".*"
    print(escaped_pattern)
    print(img_url)


    matches = re.search(escaped_pattern, img_url)
    try:
        assert matches is not None, "img_url format either has changed or the HTML structure has been changed"
    except AssertionError as e:
        print(str(e))
        return False

    return True

def find_comic(unused_comics):
    comic_num = random.choice(unused_comics)
    unused_comics.remove(comic_num)
    print("Sending comic: " + str(comic_num))

    page_url = "https://xkcd.com/" + str(comic_num) + "/"
    page = urlopen(page_url)
    soup = BeautifulSoup(page, 'html.parser')
    try:
        img_url = soup.find_all('img')[1].attrs['src']
    except Exception as e:
        # TODO replace with some better way to report error
        print("Error with finding img_url. Maybe xkcd page format changed. Listed error:")
        print(str(e))
    img_url = "https:" + img_url
    proper_form = check_url(img_url)
    if proper_form:
        return img_url
    else:
        return None


def execute_task(unused_comics, client, send_to):
    if unused_comics == []:
        sys.exit("wtf this program has been running for too long")
    img_url = find_comic(unused_comics)
    if img_url is None:
        pass
    else:
        client.send_mms(send_to, img_url)

# TODO make loop take into account new comics added after program has already begun executing

def main(client, send_to, frq):
    num_existing_comics = most_recent_comic_num()
    unused_comics = [i+1 for i in range(num_existing_comics)]

    # schedule.every(5).seconds.do(execute_task, unused_comics, client, send_to)
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
