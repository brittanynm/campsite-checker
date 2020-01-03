from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client()

def is_valid_number(number):
    try:
        response = client.lookups.phone_numbers(number).fetch(type="carrier")
        return True
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e
