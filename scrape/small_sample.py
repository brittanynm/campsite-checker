import requests
from bs4 import BeautifulSoup
import csv



#replace this with the search page on rec.gov
page = requests.get('https://www.recreation.gov/search?start=0')

soup = BeautifulSoup(page.text, 'html.parser')

# Remove bottom links
last_links = soup.find(class_='rec-flex-card-top-left-content-wrap')
last_links.decompose()

#reference the a tag for links thats reference the page that describes the site. like the campsites. Each campsite name is a reference to a link. Like the campsites

# Create a file to write to, add headers row
f = csv.writer(open('small_sample.csv', 'w'))
f.writerow(['Name', 'Link'])

# Pull all text from the BodyText div
campsite_name_list = soup.find(class_='rec-flex-card-title')

# Pull text from all instances of <a> tag within BodyText div
campsite_name_list_items = campsite_name_list.find_all('a')

# Create for loop to print out all campsites' names. Do the same with the campsite names
for campsite_name in campsite_name_list_items:
	# print(campsite_name.prettify()) originally printed all of the link content
	#instead of printing the entire link and its tag, we’ll print the list of children / the campsites’ full names
    names = campsite_name.contents[0]
    # get the URL as well WHICH CONTAINS THE CAMPSITE ID
    links = 'https://www.recreation.gov/' + campsite_name.get('href')
    # Add each campsite’s name and associated link to a row
    f.writerow([names, links])




