# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC8c5ba618686ac695cb965f2d3830354e'
auth_token = 'cc3dc5e4307e313577af1029959f7a87'
client = Client(account_sid, auth_token)

def send_text(phone, msg):
    message = client.messages \
                .create(
                     body=msg,
                     from_='+14125321330',
                     to="+1" + phone 
                 )
    pass