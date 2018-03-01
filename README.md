# daily-texts
Hello! This repo is still under active development so its exact end-form has not been determined yet. But in its current state, given a Twilio client sid and key, this program can send (1) random xkcd comics to a specified number or (2) send current cryptocurrency prices to a specified number on a regular basis.

This project currently uses Twilio's sms/mms API and a webscraping library called BeautifulSoup as well as https://xkcd.com/ and https://coinranking.com/ as source websites.

Currently for the program to run, you'd need your own Twilio account. Upload a text file into the same directory as the project named `private.txt` with exactly four lines:

1. Your Twilio Account SID
2. Your Twilio Authentication token
3. The number you'd like to send to
4. The number you're sending from (this should be a Twilio number)

After doing this, simply run `python3 temp_main.py` and simply follow the prompts after that.
