# The Project
Welcome to my first full-stack app, <strong>daily-xkcd</strong>! Users sign up through a simple website to get a text with an image scraped from xkcd's website, https://xkcd.com/ and an accompanying message at a specified time every day ( full credits to xkcd for all their great comics :) ). Visit the app here: <strong>https://daily-xkcd.herokuapp.com/</strong>.

## Design
This is a full-stack MVC-compliant app that uses the following frameworks/libraries/APIs:

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


Here's a diagram showing how my project files all interact with each other (descriptions below):

<img src=project-design.png width=80% height=auto>

### Frontend

The website you see when you visit https://daily-xkcd.herokuapp.com/ is written in HTML/CSS with Jinja2 templating syntax and served by Flask (`app.py`). The site is (you guessed it) hosted by Heroku. There are no subdomains, but the site is rendered dynamically depending on user submissions - when submissions are made, corresponding COMPLETED or ERROR pages, depending on input, are returned and served back to the root page. An example of an error would be if somebody tried to submit `abcd` or `000-000-0000` as their phone number, they would be served the ERROR page (`templates/err.html`).

Currently, all input validation is done server-side (in `server_utils.py`). Client-side validation is planned for a future release.


### Backend

There are four main components to the project backend: The sms/mms client (**Twilio**), the web scraper (**BeautifulSoup**), the database (**Google Sheets**), and the **router** (`router.py`) that delegates to/from all of them. Each file in this project was written to be readable, well-abstracted, robust, and scalable.

**--OVERALL/router--** (`router.py`)<br>
All backend processes are delegated through `router.py`. The router is called by either `app.py` when a user enters their information and submits, or by `clock.py` on regular half hour intervals. When users submit, `router.py` just passes their information along to `db_utils.py` to add an entry into the appropriate table in **Google Sheets**. The main process is run when `clock.py`, triggers. `clock.py` passes the time to `router.py`, which then does roughly the following (all in the diagram above!):
1. It passes the time to `db_utils.py`, which queries **Google Sheets** for users who signed up for the corresponding time slot, chooses a comic that hasn't been sent to that user yet, and returns that to `router.py`.
2. `router.py` passes the `comic_num` of each user to `scrape_utils.py`, which scrapes https://xkcd.com/ using **BeautifulSoup** for the corresponding `comic_url` and `comic_caption`, and returns those back to `router.py`.
3. `router.py` takes all of these values (`name`, `phone_num`, `comic_url`, `comic_caption`) and creates a `twilio_utils.MMS` (defined in `twilio_utils`) object for each user.
4. Each `twilio_utils.MMS` object is then passed to the **Twilio** client - `twilio_utils.ClientWrapper.send_mms()` - which sends the mms to its corresponding user.

Note: Heavy use of Heroku config vars was made to access sensitive information like Twilio and Google Auth API authentication keys
<br><br>
#### *Details*

**--sms/mms client--** (`twilio_utils.py`)<br>
The sms/mms client is powered by Twilio. Using Twilio's REST API, we can create `twilio.rest.Client` objects that contain a set of authenticated Twilio credentials. I made a wrapper class (called ClientWrapper) to create objects containing this client, the `send_from` phone number, and abstracted methods to simplify the process of sending messages.

**--web scraping--** (`scrape_utils.py`)<br>
BeautifulSoup was used to scrape the xkcd website's subdomains (https://xkcd.com/*) for image urls and captions, which are composed into `twilio_utils.MMS` objects that are later sent to the client to send to users.

**--database--** (`db_client.py`, `db_utils.py`, `db_setup.py`)<br>
I've gone with Google Sheets as a lightweight database - an interesting choice to many, probably. I chose Google Sheets primarily because this is my first full-stack project and Google Sheets has a really great UI, which was more comfortable for me to work with. I'm using the `gspread` and `google-auth` libraries to communicate with the Google Sheets API. For every user I only store 4 pieces of information: Name, number, number of comics sent to them, and a list of the comics sent. The second to last is just to keep some stats about the project. The last one makes sure no repeat comics are sent.

_some interesting notes on my database_
1. "lightweight database" - the cell cap for a single Google Sheets workbook is 2,000,000 and I use 4 cells per user => I can support ~500,000 users.
2. On my free plan for the Google Sheets API, I'm allotted 100 requests every 100 seconds. This might seem like an issue for scalability at first, but in fact it's not - I use batch queries and batch updates. Instead of updating cell-by-cell, I pull all the cells I need, update them locally, and send them back as one request, totaling two requests (+ misc requests for metadata checks) per update, which I only need to do once every 15-30 minutes.
3. Currently, the process for choosing a comic for a user is to randomly select one and check if it's been sent to the user before - repeat if necessary. The probability of selecting an unused comic here follows a geometric distribution with parameter `p=(# comics unseen)/(# total comics)`. With a little math (or googling), we find that the expected number of random samples we need before we find a comic we haven't used yet is `1/p`. Currently xkcd has close to 2000 comics available. This means that I'd need to send ~1000 comics to a user before the expected number of samples I'd need for that user reaches just 2. At one comic each day, that's around 3 years before we reach this benchmark. Originally, I was going to convert my list of used comics to a list of unused comics at some benchmark (e.g. maybe when EV > 10), but decided that that would happen > 5 years from now, and by then something else would probably be obsolete or I would probably have a better way to do this whole project.
4. I've written a file called db_setup.py that's never called during runtime. It was originally used for development when I needed to quickly teardown/rebuild/recustomize my Google Sheet. I've left it around in case I lose my db and I need to rebuild it, and probably because it's a nicely written file I'm proud of and I don't want to delete :)

