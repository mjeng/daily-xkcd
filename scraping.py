from urllib.request import urlopen
from bs4 import BeautifulSoup

page = urlopen("https://xkcd.com/")
soup = BeautifulSoup(page, 'html.parser')

# def scrape_test():
#     page = urlopen("https://xkcd.com/")
#     print(page)
#     soup = BeautifulSoup(page, 'html.parser')
#     print(soup)
#     print(soup.find('h1', attrs={"id": "middleContainer"}))
#
# if __name__ == "__main__":
#     scrape_test()



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
    # TODO

def test2():
    coin_dict = {}
    coin_list = soup2.find_all("div", {"class": "coin-list__body"})
    print(coin_list)
    for row in coin_list:
        name = row.find("span", {"class": "coin-name"}).string
        price = row.find("span", {"class": "coin-list__body__row__price__value"}).string
        coin_dict = {name: float(price)}
    print(coin_dict)
