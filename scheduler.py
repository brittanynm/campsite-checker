from model import *
from flask import Flask
import schedule
import requests, json, time
from twilio.rest import Client
from server import *
from api import check_availability, get_num_available_sites
from datetime import date

account_sid = 'AC8c5ba618686ac695cb965f2d3830354e'
auth_token = 'cc3dc5e4307e313577af1029959f7a87'
client = Client(account_sid, auth_token)

def job():
    '''Pulls all requests that are in the future and sorts by created_at'''
    date_today = date.today()
    subscriptions = Request.query.filter(Request.date_end < date_today)
    subscriptions = subscriptions.order_by(Request.created_at.desc())
    print(subscriptions)
    for subscription in subscriptions:
        date_start, date_end, campsite_id = subscription.date_start, subscription.date_end, subscription.campsite_id
        resp = check_availability(date_start, date_end, campsite_id)
        for site in resp["campsites"].values():
            available = bool(len(site["availabilities"]))
            if available:
                #update available column in requests to True
                Request.available = True
                #query for user phone number
                phone = Request.phone
                #send text to user
                send_text(phone)
                #remove schedule

def send_text(phone):
    message = client.messages \
                .create(
                     body='There is availability at your campsite! Go to www.recreation.gov to book as soon as possible!',
                     from_='+14125321330',
                     to='+1' + phone 
                 )

schedule.every(5).minutes.do(job)

## Look into cron jobs and job queues in python       



