from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint
import datetime
import os
import time
import pandas as pd

url = 'https://www.recreation.gov/camping/aspen-hollow-group/r/campgroundDetails.do?contractCode=NRSO&parkId=71546'


# stores today’s .now timestamp to current time and the portion of that timestamp that is today’s date in the format that the website can read it.
current_time = datetime.datetime.now()
current_time.strftime("%m/%d/%Y")

# define how many nights to stay at the campsite, how far from now to look, how many weekends I’d like to check:
nights_stay = 2
weeks_from_now_to_look = 13
how_many_weeks_to_check = 4


for week in range(0, how_many_weeks_to_check):
    start_date = current_time + datetime.timedelta(days=week*7) + datetime.timedelta(days=weeks_from_now_to_look*7)
    end_date = start_date + datetime.timedelta(days=nights_stay)
    print(start_date.strftime("%a %b %d %Y") + ' to ' + end_date.strftime("%a %b %d %Y"))