# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/user/account

client = Client(account_sid, auth_token)

message = client.messages.create(
    "",
    body="Hellooooo dis is matthieu. pls lmk if you got this",
    from_="",
    media_url="https://i.imgur.com/9JE4oOm.png"
)

print(message.sid)
