import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# import server

BASE_URL = "http://www.recreation.gov"
AVAILABILITY_ENDPOINT = "/api/camps/availability/campground/"

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"

headers = {"User-Agent": user_agent}


def check_availability(date_start, date_end, site_id):
    """Send availability request to recreation.gov"""
    query = (
        "?start_date="
        + date_start.strftime("%Y-%m-%d")
        # + date_start
        + "T00%3A00%3A00.000Z&end_date="
        + date_end.strftime("%Y-%m-%d")
        # + date_end
        + "T00%3A00%3A00.000Z"
    )

    url = BASE_URL + AVAILABILITY_ENDPOINT + site_id + query
    resp = requests.get(url, headers=headers)

    return resp.json()


def get_num_available_sites(resp, date_start, date_end):
    """Using the API response, return number of sites available out of total sites"""
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
    return f"{num_available} site(s) available out of {maximum} site(s)"

