from urllib.request import urlopen
from bs4 import BeautifulSoup
from twilio.rest import Client
import time
import sys
import random
import schedule

# TODO: IMPORTANT redo git commits - need to remove personal number, account_sid, auth_token
# TODO: switch from list to text file to store used comics
# TODO: ^^in conjunction with this switch the program to sth that only
# has to run periodically and not be constantly on
# TODO: try git branch
# TODO: figure out how to take text feedback from person receiving text
# and implement a STOP option + other stuff
# TODO: maybe make this into a hw reminder kind of app too

def find_comic(used_comics):
    comic_num = random.choice(used_comics)
    used_comics.remove(comic_num)

    page_url = "https://xkcd.com/" + str(comic_num) + "/"
    page = urlopen(page_url)
    soup = BeautifulSoup(page, 'html.parser')
    img_url = soup.find_all('img')[1].attrs['src']
    img_url = "https:" + img_url

    return img_url


def send_comic(comic_url, client):
    message = client.messages.create(
        "",
        from_="",
        media_url=comic_url
    )


def execute_task(used_comics, client):
    print(used_comics)
    if used_comics == []:
        sys.exit("wtf this program has been running for too long")
    img_url = find_comic(used_comics)
    send_comic(img_url, client)



def main():
    num_existing_comics = 1953
    used_comics = [i+1 for i in range(num_existing_comics)]

    account_sid = ""
    auth_token = ""
    client = Client(account_sid, auth_token)

    schedule.every(5).seconds.do(execute_task, used_comics, client)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit("\nExiting program\n")



if __name__ == "__main__":
    main()
