import server_utils
import twilio.rest
import random


class SMS:

    def __init__(self, phone_num, message):
        assert isinstance(phone_num, str), "Phone number needs to be a string"
        assert isinstance(message, str), "Message needs to be a string"
        self.phone_num = phone_num
        self.message = message


class MMS:

    CAPTION_NAME = [
        "Hi {0}! Here's your xkcd comic:\n{1}",
        "Here you go {0}:\n{1}"
    ]
    CAPTION = [
        "{1}\n\nHope your day is going well!",
        "{1}\n\nHope today is a good day!",
        "Here you go:\n{1}",
        "Caption:\n{1}\nHave a good day :)",
        "Caption:\n{1}"
        ":o\n{1}",
        "{1}",
        "Enjoy!\n{1}"
    ]
    NAME = [
        "Hey {0}. Here's your daily comic!",
        "Have a great day {0}!",
        "Hope you have a great day {0}!",
        "Have a nice day {0}!"
    ]
    NONE = [
        ":)",
        ":D",
        ":0",
        "c:",
        ".  .\n  v",
        "Have a great day!",
        "I hope your day is going great!",
        "Have a swell day!",
        "Hope this brightens your day!",
        "Have a good day!",
        "Have a nice day :)"
    ]

    def __init__(self, name, phone_num, comic_num):

        try:
            int(comic_num)
        except ValueError:
            server_utils.log("Comic number needs to be able to be converted to int when creating MMS object")
            return

        try:
            assert isinstance(name, str), "Name needs to be a string when creating MMS object"
            assert isinstance(phone_num, str), "Phone number needs to be a string when creating MMS object"
        except AssertionError as e:
            server_utils.log(e)
            return

        self.name = name
        self.phone_num = phone_num
        self.comic_num = int(comic_num)
        self.comic_url = None
        self.message = ''
        self.updated = False

    def update(self, url, caption):

        assert bool(url), "URL must have a value"

        self.comic_url = url

        if caption and self.name:
            greeting = random.choice(MMS.CAPTION_NAME + MMS.CAPTION)
        elif self.name:
            greeting = random.choice(MMS.NAME + MMS.NONE)
        elif caption:
            greeting = random.choice(MMS.CAPTION + MMS.NONE)
        else:
            greeting = random.choice(MMS.NONE)

        self.message = greeting.format(self.name, caption)

        self.updated = True


class ClientWrapper:

    def __init__(self, account_sid, auth_token, my_num):
        assert isinstance(my_num, str), "Sender must be a number converted to string"
        self.client = twilio.rest.Client(account_sid, auth_token)
        self.num = my_num

    def send_sms(self, sms):
        assert isinstance(sms, SMS), "sms needs to be an SMS object"
        self.client.messages.create(
            sms.phone_num,
            from_=self.num,
            body=sms.message
        )
        server_utils.log("Sent SMS with body: {0}".format(sms.message))

    def send_mms(self, mms):
        assert isinstance(mms, MMS), "mms needs to be an MMS object"
        assert mms.updated == True, "mms not updated with message and/or url"

        self.client.messages.create(
            mms.phone_num,
            from_=self.num,
            body=mms.message,
            media_url=mms.comic_url
        )
        server_utils.log("Sent MMS to {0} with media {1} and body: {2}".format(mms.name, mms.comic_url, mms.message))
