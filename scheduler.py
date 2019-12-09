from model import *
from flask import Flask
import schedule
import requests, json, time
from server import *
from api import check_availability, get_num_available_sites
from datetime import date
from twilio.rest import Client
import os

app = Flask(__name__)
connect_to_db(app)

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def job():
    """Pulls all requests that are in the future and checks availability"""
    date_today = date.today()
    subscriptions = (
        Request.query.filter(Request.date_end > date_today, Request.sms_sent == False)
        .order_by(Request.created_at.desc())
        .all()
    )
    print(subscriptions)
    for subscription in subscriptions:
        date_start, date_end, campsite_id = (
            subscription.date_start,
            subscription.date_end,
            subscription.campsite_id,
        )
        resp = check_availability(date_start, date_end, campsite_id)
        for site in resp["campsites"].values():
            # available = bool(len(site["availabilities"]))
            for status in site["availabilities"].values():
                if status == "Available":
                    subscription.available = True
                    db.session.add(subscription)
                    db.session.commit()
                    break
        if subscription.available == True:
            user_id = User.query.filter(User.user_id == subscription.user_id).one()
            phone = user_id.phone
            site= subscription.campsite_id
            send_text(phone, site)
            subscription.sms_sent = True
            # db.session.add(subscription)
            db.session.commit()


def send_text(phone, site):
    """Sends user a text letting them know their is availability"""
    print("Send text")
    message = client.messages.create(
        body="There is availability for one of your campsites! Go to https://www.recreation.gov/camping/campgrounds/" + site + "/availability to book it as soon as possible!",
        from_="+14125321330",                  
        to="+1" + phone,
    )


schedule.every(10).seconds.do(job)

while True:
    print("Check")
    schedule.run_pending()
    time.sleep(1)
