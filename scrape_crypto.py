from urllib.request import urlopen
from bs4 import BeautifulSoup



def find_recent_prices():
    website = "https://coinranking.com/"
    page = urlopen(website)
    soup = BeautifulSoup(page, 'html.parser')

    coin_dict = {}
    coin_list_body = soup2.find("div", {"class": "coin-list__body"})
    coin_list = coin_list_body.find_all("a", {"class": "coin-list__body__row"})

    for row in coin_list:
        name = row.find("span", {"class": "coin-name"}).string
        price = row.find("span", {"class": "coin-list__body__row__price__value"}).string
        price = remove_comma(price)
        price = float(price)
        coin_dict[name] = price

    return coin_dict


def send_prices():
    return None


def execute_task(which_coins, client, send_to):
    """
    which_coins: list of (type str) coin names to send
    client: sender.MyClient object
    send_to: string of number to send to
    """
    return None


def main(client, send_to):
    return None
