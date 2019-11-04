import requests


# API information
BASE_URL = "http://www.recreation.gov"
AVAILABILITY_ENDPOINT = "/api/camps/availability/campground/"
MAIN_PAGE_ENDPOINT = "/api/camps/campgrounds/"

INPUT_DATE_FORMAT = "%Y-%m-%d"

# FUNCTION IDEAS 
# format_date
# generate start date and end date
# send request
# get park information
# get campsite id
# get num of available sites
# validate dates entered are in the future
# validate phone number entered
# check avialability (main)


def get_campsite_id(campsite_name):
    campsite_name = resp['campground']['facility_name']
    # if the required information is in the request, look for campsite

    # FIX ME: look up campsite id with name

    if selected_campsite:
        payload - {}
        headers = {}
        response = requests.get()
        data = response.json()

        # How can I package all of this info at the end when phone is submitted?

        # store selected site in database
        campsite = Request(selected_campsite=name)

        # Use selected campsite to look up campsite ID and store in DB
        db.session.add(campsite)
        db.session.commit()
        
    return campsite_id


def format_date(date_obj):
    # FIX ME

    #return formatted_date


def valid_dates():
    # FIX ME
    #if current_date > date_start OR if invalid format:
        # flash("Select a valid date ")


def generate_params(start, end):
    # FIX ME

    #return params


def send_request(url, params):
    # payload = {}
    # request = requests.get(url, params=payload)

    # return response.json


def get_campsite_information(campsite_id, params):
    url = "{}{}{}".format(BASE_URL, AVAILABILITY_ENDPOINT, site_id)

    return send_request(url, params)


def num_of_available_sites(resp, start_date, end_date):
    # FIX ME

    #return num_available, total_sites


def main(campsite_id // campsite_name):
    # FIX ME -- which arg to pass?

    #return what is available or sold out


def seed_db():
