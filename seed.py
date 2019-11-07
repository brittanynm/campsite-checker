# import requests

# URL = "https://www.recreation.gov/api/search"

# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

# headers = {'User-Agent': user_agent}

# def seed():
#     payload = {
#                 "exact": False,
#                 "size": 100,
#                 "fq": "entity_type:campground",
#                 "start": 0
#                 }

#     response = requests.get(URL, params=payload)
#     print(response.content)
#     print(response.request.url)

#     while "results" in response.json():
#         result = response.json()
#         print(result.keys())
#         payload["start"] += 1000
#         response = requests.get(URL, params=payload, headers=headers)

		# campsite = Campsite(name=name)

		# db.session.add(campsite)
		# db.session.commit()
# seed()


import requests
import json
import csv

from sqlalchemy import func
from model import User, Campsite, Request, connect_to_db, db
from server import app

def load_campsites():
    print("Campsites")

    for row in open("seed.csv", encoding='cp1252'):
        row = row.rstrip()
        site_id, name, park = row.split(",")

        campsite = Campsite(id=site_id,
                    name=name,
                    park=park)

        # We need to add to the session or it won't ever be stored
        db.session.add(campsite)

    # Once we're done, we should commit our work
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    load_campsites()

# f = csv.writer(open('fifth.csv', 'w'))
# f.writerow(['ID', 'Name', 'Park'])

# response = open("fifth.json")
# response = json.load(response)

# for item in response["results"]:
#     campsite_id = item["entity_id"]
#     campsite_name = item["name"]
#     if item.get("parent_name", None) == None:
#         continue
#     else:
#         park = item["parent_name"]
#     # directions = item["directions"]
#     # if item.get("preview_image_url", None) == None:
#     #     continue
#     # else:
#     #     preview_img = item["preview_image_url"]
    
#     # if item.get("city", None) == None:
#     #     continue
#     # else:
#     #     city = item["city"]
#     f.writerow([campsite_id, campsite_name, park])



