from urllib.request import urlopen
from bs4 import BeautifulSoup

page = urlopen("https://xkcd.com/")
soup = BeautifulSoup(page, 'html.parser')


def test():
    # can also use soup.find("sth", {"class": sth, "id": sth})
    tag = soup.find("div", id="news")
    print(tag.string)
    tag.string = "\nhello\n"
    print(tag.string)
    tag.string.replace_string_with("\nanother hello\n")
    print(tag.string)
    print(soup.div)

    # can reassign ids, classes etc. classes come in list form bc can have >1
    soup.div['id'] = 'bleh'

page2 = urlopen("https://coinranking.com/")
soup2 = BeautifulSoup(page2, 'html.parser')

def remove_comma(s):
    new_str = ''
    for c in s:
        if c != ',':
            new_str += c
    return new_str


def test2():
    coin_dict = {}
    coin_list_body = soup2.find("div", {"class": "coin-list__body"})
    coin_list = coin_list_body.find_all("a", {"class": "coin-list__body__row"})

    for row in coin_list:
        name = row.find("span", {"class": "coin-name"}).string
        price = row.find("span", {"class": "coin-list__body__row__price__value"}).string
        price = remove_comma(price)
        price = float(price)
        coin_dict[name] = price

    print(coin_dict)
