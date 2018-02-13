import schedule
import send
import scrape_xkcd
import scrape_crypto

# TODO: IMPORTANT redo git commits - need to remove personal number, account_sid, auth_token
# TODO: switch from list to text file to store used comics
# TODO: ^^in conjunction with this switch the program to sth that only
# has to run periodically and not be constantly on
# TODO: try git branch
# TODO: figure out how to take text feedback from person receiving text
# and implement a STOP option + other stuff
# TODO: maybe make this into a hw reminder kind of app too


# currently using this for testing purposes while being able to commit to repository
# probably won't keep format later on
if __name__ == "__main__":
    f = open("private.txt", 'r')
    account_sid = f.readline()[:-1] # to get rid of \n
    auth_token = f.readline()[:-1]
    send_to = f.readline()[:-1]
    send_from = f.readline()[:-1]
    print(send_to)
    print(send_from)
    client = send.MyClient(account_sid, auth_token, send_from)

    option = int(input("Choose an option:\n(1) execute scrape_xkcd\n(2) execute scrape_crypto\n"))
    assert option == 1 or option == 2, "Not valid option"

    if option == 1:
        scrape_xkcd.main(client, send_to)
    elif option == 2:
        scrape_crypto.main(client, send_to)
