import requests
from bs4 import BeautifulSoup
import csv



#replace this with the search page on rec.gov
page = requests.get('https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ1.htm')

soup = BeautifulSoup(page.text, 'html.parser')

# Remove bottom links
last_links = soup.find(class_='AlphaNav')
last_links.decompose()

#reference the a tag for links thats reference the page that describes the site. like the campsites. Each campsite name is a reference to a link. Like the campsites

# Create a file to write to, add headers row
f = csv.writer(open('art_example.csv', 'w'))
f.writerow(['Name', 'Link'])

# Pull all text from the BodyText div
artist_name_list = soup.find(class_='BodyText')

# Pull text from all instances of <a> tag within BodyText div
artist_name_list_items = artist_name_list.find_all('a')

# Create for loop to print out all artists' names. Do the same with the campsite names
for artist_name in artist_name_list_items:
	# print(artist_name.prettify()) originally printed all of the link content
	#instead of printing the entire link and its tag, we’ll print the list of children / the artists’ full names
    names = artist_name.contents[0]
    # get the URL as well WHICH CONTAINS THE CAMPSITE ID
    links = 'https://web.archive.org' + artist_name.get('href')
    # Add each artist’s name and associated link to a row
    f.writerow([names, links])




