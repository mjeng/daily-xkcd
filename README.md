# daily-xkcd
Hello! This repo is still under active development. The plan is to have a website where a user can sign up and begin receiving daily texts at a specified time during the day. The website is in HTML/CSS and will use PHP to connect to a MySQL database. The messaging script is written in Python. In its current state, given a Twilio client sid and key, this program can send random xkcd comics to a specified number to a specified number on a regular basis.

This project currently uses Twilio's sms/mms API and a webscraping library called BeautifulSoup as well as https://xkcd.com/ as a source website.

Currently for the program to run, you'd need your own Twilio account. Upload a text file into the same directory as the project named `private.txt` with exactly four lines:

1. Your Twilio Account SID
2. Your Twilio Authentication token
3. The number you'd like to send to
4. The number you're sending from (this should be a Twilio number)

After doing this, simply run `python3 temp_main.py` and follow the prompts after that.
