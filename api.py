import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

#search URL
# base_search_url = "https://ridb.recreation.gov/api/vi/campsites"

# API availability information
BASE_URL = "http://www.recreation.gov"
AVAILABILITY_ENDPOINT = "/api/camps/availability/campground/"
MAIN_PAGE_ENDPOINT = "/api/camps/campgrounds/"

INPUT_DATE_FORMAT = "%Y-%m-%d"

# FUNCTION IDEAS 
# generate start date and end date
# send request
# get park information
# get campsite id
# get num of available sites
# validate dates entered are in the future
# validate phone number entered
# check avialability (main)


def get_campsite_id(campsite_name):
    # FIX ME: look up campsite id with name
    SELECT campsite_id FROM campsites WHERE campsite_name=name

        # store selected site in database
        campsite = Request(selected_campsite=name)

        # Use selected campsite to look up campsite ID and store in DB
        db.session.add(campsite)
        db.session.commit()
        
    return campsite_id


def generate_params(start, end):
    # From HTML calendar, pass selected dates into database and into availability checker

    #return formatted params


def send_avail_request(url, params):
    payload = {}
    request = requests.get(url, params=payload)

    return response.json


def num_of_available_sites(resp, start_date, end_date):
    # pass start and end dates and the response from the api

    #return num_available, total_sites


def main(campsite_id):

    #return what is available or sold out


def seed_db():
