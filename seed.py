"""Parse data from API and store into database"""

from pprint import pprint
# make json file more readable
import json
# Needed to make API Requests
import requests
# No API key needed
URL = "https://api.covid19api.com/country/us/status/confirmed"
URL2 = "https://api.covid19api.com/country/us/status/deaths"

def get_confirmed_reports():
    """Returns confirmed reports of COVID-19 in each state."""

    r1 = requests.get(URL)
    return r1
get_confirmed_reports()