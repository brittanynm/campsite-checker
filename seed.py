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



import json

response = open("first_1thousand.json")
response = json.load(response)
campsite_name = (response['results'][0]['entity_id'])
# print(response.keys())
print("\n\n\n")

for item in response["results"]:
    campsite_id = item["entity_id"]
    campsite_name = item["name"]
    directions = item["directions"]
    if item.get("preview_image_url", None) == None:
        continue
    else:
        preview_img = item["preview_image_url"]
    
    if item.get("city", None) == None:
        continue
    else:
        city = item["city"]
    
    if item.get("parent_name", None) == None:
        continue
    else:
        park = item["parent_name"]
    f.writerow([campsite_id, campsite_name, park, preview_image_url, directions, city])

#use directions, reservable, city, description, preview_image_url
#look into 'rate' further and pprint


# for item in response:
    #look into response.json.keys()
