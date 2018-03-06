import schedule
import sender
import scrape_xkcd

# TODO: ^^in conjunction with this switch the program to sth that only
# has to run periodically and not be constantly on
# TODO: try git branch
# TODO: figure out how to take text feedback from person receiving text
# and implement a STOP option + other stuff
# TODO: maybe make this into a hw reminder kind of app too
# TODO: try Docker for deployment
# TODO: build frontend

# currently using this for testing purposes while being able to commit to repository
# probably won't keep format later on
if __name__ == "__main__":
    f = open("private.txt", 'r')
    account_sid = f.readline()[:-1] # to get rid of \n
    auth_token = f.readline()[:-1]
    send_to = f.readline()[:-1]
    send_from = f.readline()[:-1]
    print("Sending to: " + send_to + " from " + send_from)
    client = sender.MyClient(account_sid, auth_token, send_from)

    option = print("Executing scrape_xkcd\n")

    frq_specs = {}
    units_option = int(input("Choose a unit of time:\n(1) seconds\n(2) minutes\n(3) hours\n(4) days\n"))
    assert units_option in [1, 2, 3, 4], "Not valid option"
    if units_option == 1:
        frq_specs['units'] = "seconds"
    if units_option == 2:
        frq_specs['units'] = "minutes"
    if units_option == 3:
        frq_specs['units'] = "hours"
    if units_option == 4:
        frq_specs['units'] = "days"

    num_option = input("Every how many " + frq_specs['units'] + " would you like your message to send (number)? ")
    try:
        frq_specs['num'] = int(num_option)
    except Exception as e:
        print("Invalid input. Error:")
        print(str(e))

    scrape_xkcd.main(client, send_to, frq_specs)
