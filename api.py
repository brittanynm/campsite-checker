import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
# import server

# API availability information
BASE_URL = "http://www.recreation.gov"
AVAILABILITY_ENDPOINT = "/api/camps/availability/campground/"

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

headers = {'User-Agent': user_agent}


def availability(date_start, date_end, site_id):
    q = "?start_date=" + date_start + "T00%3A00%3A00.000Z&end_date=" + date_end + "T00%3A00%3A00.000Z"
    url = BASE_URL + AVAILABILITY_ENDPOINT + site_id + q

    resp = requests.get(url, headers=headers)
    
    return resp.json()


def get_num_available_sites(resp, start_date, end_date):
    maximum = resp["count"]
    num_available = 0
    
    for site in resp["campsites"].values():
        available = bool(len(site["availabilities"]))
        for key, status in site["availabilities"].items():
            if status != "Available":
                available = False
                break
        if available:
            num_available += 1
    print(num_available, "site(s) available out of", maximum, "site(s)")


resp = availability('2019-12-01', '2019-12-04', '234513')
get_num_available_sites(resp, '2019-12-01', '2019-12-04')


# def send_avail_request(url, params):
#     payload = {}
#     request = requests.get(url, params=payload)

#     return response.json





# def seed_db():
