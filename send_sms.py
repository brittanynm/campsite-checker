# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

client = Client(account_sid, auth_token)

def send_text(phone, msg):
    message = client.messages \
                .create(
                     body=msg,
                     from_='+14125321330',
                     to="+1" + phone 
                 )
    pass