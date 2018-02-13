import send
import scrape_crypto




if __name__ == "__main__":
    f = open("private.txt", 'r')
    account_sid = f.readline()[:-1] # to get rid of \n
    auth_token = f.readline()[:-1]
    my_num = f.readline()[:-1]
    send_from = f.readline()[:-1]
    print(account_sid + "\n" + auth_token + "\n" + str(my_num) + "\n" + send_from)
