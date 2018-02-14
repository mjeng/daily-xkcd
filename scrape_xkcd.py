from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import sys
import random
import schedule
import re


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
    m = re.search(regex_str, perm_link)
    comic_num = m.group(0)[len(main_website):][:-1]

    return int(comic_num)


def find_comic(used_comics):
    comic_num = random.choice(used_comics)
    used_comics.remove(comic_num)
    print("Sending comic: " + str(comic_num))

    page_url = "https://xkcd.com/" + str(comic_num) + "/"
    page = urlopen(page_url)
    soup = BeautifulSoup(page, 'html.parser')
    img_url = soup.find_all('img')[1].attrs['src']
    img_url = "https:" + img_url

    return img_url


def execute_task(used_comics, client, send_to):
    if used_comics == []:
        sys.exit("wtf this program has been running for too long")
    img_url = find_comic(used_comics)
    client.send_mms(send_to, img_url)


def main(client, send_to):
    num_existing_comics = most_recent_comic_num()
    used_comics = [i+1 for i in range(num_existing_comics)]

    schedule.every(5).seconds.do(execute_task, used_comics, client, send_to)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit("\nExiting program\n")
