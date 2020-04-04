"""Parse data from API and store into database"""

from pprint import pprint
# make json file more readable
import json
# Needed to make API Requests, threading, etec
import requests, os, bs4, threading, time
# No API key needed
URL = "https://api.covid19api.com/country/us/status/confirmed"
URL2 = "https://api.covid19api.com/country/us/status/deaths"

# Read Only (‘r’): Open text file for reading.
# Write Only (‘w’): Open the file for writing.
# Append Only (‘a’): Open the file for writing. The data being written will be inserted at the end, after the existing data.
# Read and Write (‘r+’): Open the file for reading and writing.


def get_covid_status():
    """Writes confirmed/death reports of COVID-19 in each state to txt file."""
    r1 = requests.get(URL)
    r2 = requests.get(URL2)

    # Confirmed
    # Convert JSON data to python data structure
    confirmed_data = json.loads(r1.text)
    out_file = open("confirmed-reports.txt", "w")
    json.dump(confirmed_data, out_file, indent=6)
    out_file.close()

    # Deaths
    deaths_data = json.loads(r2.text)
    out_file = open("death-reports.txt", "w")
    json.dump(deaths_data, out_file, indent=6)
    out_file.close()


api_requests = []
for i in range(0, 7):   # loop 7 times
    callAPI = threading.Thread(target=get_covid_status)
    api_requests.append(callAPI)  # keep track of thread object created
    callAPI.start()
    print("starting") 
    time.sleep(86400)   # pause for 24 hrs
    print()
    print('Reeee')

# Notify when all threads end
for call_api in api_requests:
    call_api.join()

print('Completed tasks for the week!')