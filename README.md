# The Project
Welcome to my first full-stack app, <strong>daily-xkcd</strong>! Users sign up through a simple website to get a text with an image scraped from xkcd's website, https://xkcd.com/ and an accompanying message at a specified time every day ( full credits to xkcd for all their great comics :) ). Visit the app here: <strong>https://daily-xkcd.herokuapp.com/</strong>.

## Design/In-depth Description/I hope recruiters read this :^)
This is a full-stack app that uses the following frameworks/libraries/APIs:

(frontend)<br>
* HTML/CSS with Jinja2 templating
* Flask
* Heroku

(backend)<br>
* Python
* Google Sheets API
* Google Auth
* Twilio API
* BeautifulSoup

<img src=design.png>

### Frontend

The website you see when you visit https://daily-xkcd.herokuapp.com/ is written in HTML/CSS with Jinja2 templating syntax and served by Flask. The site is (as you've guessed) hosted by Heroku. There are no valid subdomains, but the site is rendered dynamically depending on user submissions - when submissions are made, corresponding COMPLETED or ERROR pages, depending on input, are returned and served back to the root page. An example of an error would be if somebody tried to submit "abcd" as their phone number.

Currently, all input validation is done server-side. Client-side validation is planned for a future release.


### Backend

There are four main components to the project backend: The sms/mms client (`Twilio`), the web scraper (`BeautifulSoup`), the database (`Google Sheets`), and the `router` that delegates to/from all of them. Each file in this project was written to be readable, well-abstracted, robust, and scalable (although I have no plans to scale up this project).

Heavy use of Heroku config vars was made to access sensitive information like Twilio and Google Auth authentication keys


**--sms/mms client--** (`twilio_utils.py`)<br>
The sms/mms client is powered by Twilio. Using Twilio's REST API, we can create `twilio.rest.Client` objects that contain a set of authenticated Twilio credentials. I made a wrapper class (called ClientWrapper) to create objects containing this client, the `send_from` phone number, and abstracted methods to simplify the process of sending messages.

**--web scraping--** (`scrape_utils.py`)<br>
BeautifulSoup was used to scrape the xkcd website's subdomains (https://xkcd.com/*) for image urls and captions, which are later sent to the MMS client to compose and send.

**--database--** (`db_client.py`, `db_utils.py`, `db_setup.py`)<br>
I've gone with Google Sheets as a lightweight database - an interesting choice to many, probably. I chose Google Sheets because (1) this is my first full-stack project and Google Sheets has a really great UI, which was more comfortable for me to work with, and (2) I think it's cool that you can interact with Google Sheets through code! I'm using the `gspread` and `google-auth` (originally `oauth2client` until I found out that was deprecated) libraries to communicate with the Google Sheets API. My sheet

_some interesting notes on my database_
1. "lightweight database" - the cell cap for a single Google Sheets workbook is 2,000,000 and I use 6 cells per user => I can support >300,000 users.
2. On my free plan for the Google Sheets API, I'm allotted 100 requests every 100 seconds. This might seem like an issue for scalability at first, but in fact it's not - I use batch queries and batch updates. Instead of updating cell-by-cell, I pull all the cells I need, update them locally, and send them back as one request, totaling two requests (+ misc requests for metadata checks) per update, which I only need to do once every 15-30 minutes.
3. Currently, the process for choosing a comic for a user is to randomly select one and check if it's been sent to the user before - repeat if necessary. The probability of selecting an unused comic here follows a geometric distribution with parameter `p=(# comics unseen)/(# total comics)`. With a little math (or googling), we find that the expected number of random samples we need before we find a comic we haven't used yet is `1/p`. Currently xkcd has close to 2000 comics available. This means that I'd need to send ~1000 comics to a user before the expected number of samples I'd need for that user reaches just 2. At one comic each day, that's around 3 years before we reach this benchmark. Originally, I was going to convert my list of used comics to a list of unused comics at some benchmark (e.g. maybe when EV > 10), but decided that that would happen > 5 years from now, and by then something else would probably be obsolete or I would probably have a better way to do this whole project, or something else.
4. I've written a file called db_setup.py that's never called during runtime. It was originally used for development when I needed to quickly teardown/rebuild/recustomize my Google Sheet. I've left it around in case I lose my db and I need to rebuild it, and probably more because it's a nicely written file I'm proud of and I don't want to delete :)

