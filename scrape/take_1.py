import requests
from bs4 import BeautifulSoup
import csv
# FIX ME - Add national park as well


# headers = {
#     'User-Agent': 'Brittany, example.com',
#     'From': 'email@example.com'
# }

# url = 'https://example.com'

# page = requests.get(url, headers = headers)

f = csv.writer(open('take_1.csv', 'w'))
f.writerow(['Name', 'Link'])

pages = []

for i in range(0, 222):
	pg = 0
    url = 'https://www.recreation.gov/search?start=' + str(pg)
    pages.append(url)
    pg += 20


for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='rec-flex-card-title')
    last_links.decompose()

    campsite_name_list = soup.find(class_='rec-flex-card-title')
    campsite_name_list_items = campsite_name_list.find_all('a')

    for campsite_name in campsite_name_list_items:
        names = campsite_name.contents[0]
        links = 'https://web.archive.org' + campsite_name.get('href')

        f.writerow([names, links])
