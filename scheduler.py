from model import *
from flask import Flask
import schedule
import requests, json, time
from server import *
from api import check_availability, get_num_available_sites
from datetime import date
from twilio.rest import Client
import os

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def job():
    '''Pulls all requests that are in the future and checks availability'''
    date_today = date.today()
    subscriptions = Request.query.filter(Request.date_end > date_today, Request.available == False).all()
    # subscriptions = subscriptions.order_by(Request.created_at.desc())
    for subscription in subscriptions:
        date_start, date_end, campsite_id = subscription.date_start, subscription.date_end, subscription.campsite_id
        resp = check_availability(date_start, date_end, campsite_id)
        for site in resp["campsites"].values():
            available = bool(len(site["availabilities"]))
            if available:
                #update available column in requests to True
                subscription.available = True
                #query for user phone number
                user_id = User.query.filter(User.user_id == subscription.user_id).one()
                phone = user_id.phone
                #send text to user
                send_text(phone)
                

def send_text(phone):
    '''Sends user a text letting them know their is availability'''
    message = client.messages \
                .create(
                     body='There is availability at your campsite! Go to www.recreation.gov to book as soon as possible!',
                     from_='+14125321330',
                     to='+1' + phone 
                 )

schedule.every(5).minutes.do(job)

## Look into cron jobs and job queues in python       




