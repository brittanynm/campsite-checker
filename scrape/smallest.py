import requests
from bs4 import BeautifulSoup


# Collect and parse first page
page = requests.get('https://www.recreation.gov/search?start=0')
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the BodyText div
campsite_name_list = soup.find(class_='rec-flex-card-top-left-content-wrap')

# Pull text from all instances of <a> tag within BodyText div
campsite_name_list_items = campsite_name_list.find_all('a')

for campsite_name in campsite_name_list_items:
    print(campsite_name.prettify())