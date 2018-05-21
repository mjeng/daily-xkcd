from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

MAIN_SITE = "https://xkcd.com/"

def most_recent_comic_num():

    page = urlopen(MAIN_SITE)

    # Whole document
    soup = BeautifulSoup(page, 'html.parser')

    # Middle container containing comic and header/footer
    middle_container = soup.find("div", {"id": "middleContainer"})

    # Permanent link is located after an empty <br> tag
    # Finding <br> tag then taking next element
    perm_link = middle_container.find("br").next_sibling

    # Regex to get number out of perm_link
    regex_str = MAIN_SITE + ".*/"
    match = re.search(regex_str, perm_link)
    comic_num = match.group(0)[len(MAIN_SITE):][:-1]

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

    matches = re.search(escaped_pattern, img_url)
    try:
        assert matches is not None, "img_url format either has changed or the HTML structure has been changed"
    except AssertionError as e:
        print(str(e))
        return False

    return True

def find_comic_url(comic_num):
    page_url = MAIN_SITE + str(comic_num) + "/"
    page = urlopen(page_url)
    soup = BeautifulSoup(page, 'html.parser')

    try:
        comic_div = soup.find('div', {'id': 'comic'})
        img_url = comic_div.find('img').attrs['src']
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

def find_comic_caption(comic_num):
    page_url = MAIN_SITE + str(comic_num) + "/"
    page = urlopen(page_url)
    soup = BeautifulSoup(page, 'html.parser')

    try:
        comic_div = soup.find('div', {'id': 'comic'})
        img_caption = comic_div.find('img').attrs['title']
    except Exception as e:
        # TODO replace with some better way to report error
        print("Error with finding img_caption. Maybe xkcd page format changed. Listed error:")
        print(str(e))

    return img_caption
