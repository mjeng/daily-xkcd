from twilio.rest import Client

class MyClient:

    def __init__(self, account_sid, auth_token, my_num):
        assert isinstance(my_num, str), "Sender must be a number converted to string"
        self.client = Client(account_sid, auth_token)
        self.num = my_num

    def send_sms(self, dest_num, message):
        assert isinstance(destination, str), "Destination must be a number converted to string"
        self.client.messages.create(
            dest_num,
            from_=self.num,
            body=message
        )

    def send_mms(self, dest_num, media_link, message=''):
        if message:
            self.client.messages.create(
                dest_num,
                from_=self.num,
                body=message,
                media_url=media_link
            )
        else:
            self.client.messages.create(
                dest_num,
                from_=self.num,
                media_url=media_link
            )
