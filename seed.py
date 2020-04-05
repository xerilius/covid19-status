"""Parse data from API and store into database"""

from pprint import pprint
# make json file more readable
import json
# Needed to make API Requests, threading, etec
import requests, os, bs4, threading, time
# No API key needed
URL = "https://api.covid19api.com/country/us/status/confirmed"
URL2 = "https://api.covid19api.com/country/us/status/deaths"

confirmed_json = "confirmed-reports.json"
deaths_json = "death-reports.json"

# JSON Data Saved in json file
def write_confirmed_data():
    """Writes confirmed/death reports of COVID-19 in each state to txt file."""
    r1 = requests.get(URL)
    with open('confirmed-reports.txt', 'w') as f:
        f.write(r1.text)

    print('task done')
# write_confirmed_data()   


def write_death_data(json):
    r2 = requests.get(URL2)
    # # Deaths
    with open('deaths-reports.txt', 'w') as f:
        f.write(r2.text)
    # deaths_data = json.loads(r2.text)
    # out_file = open(json, "w")
    # json.dump(deaths_data, out_file, indent=4)
    # out_file.close()


def extract_confirmed_data():
    """Temporary dictionary to organize data before transferring into db"""

    response = requests.get(URL)
    response.raise_for_status()
    data_=json.loads(response.text)
    w = data_

    api_data = {
        'state': None,
        'city': None,
        'cases': [],
        'date': [],
    }

    for dictionaries in w:
        # dictionaries = all dictionaries in the list
        print(dictionaries)
        
        cities = dictionaries[x]
        print(cities)
        # for key in dictionaries:

        #     states = dictionaries.get("Province")
        #     api_data['state'] = states

        #     # cities = dictionaries.get("City")
        #     # api_data['city'].append(cities)

        #     # cases = dictionaries.get("Cases")
        #     # api_data['cases'].append(cases)

        #     # date = dictionaries.get("Date")
        #     # api_data['date'].append(date)
            
            
            
    

    
    # for txt_data in json_file:
    #     state_name = txt_data['Province']
    #     api_data['state'] = state_name

    #     city_name = txt_data['City']
    #     api_data['city'] = city_name

    #     cases = txt_data['Cases']
    #     api_data['cases'] = cases

    #     status_date = txt_data['Date']
    #     api_data['date'] = status_date

    #     print(api_data)

extract_confirmed_data()



if __name__ == "__main__":

    def run_task():
        """Run task 7 times"""
        for i in range(0,1):
            t1 = threading.Thread(target=get_confirmed_status, args=(confirmed_txt,))
            t2 = threading.Thread(target=get_death_status, args=(deaths_txt,))
            # start thread 
            t1.start()
            print("t1 started")
            t2.start()
            print("t2 started")

            # time.sleep(1440)   
            # wait until threads are completely executed
            t1.join()
            t2.join()
            # both threads are completely executed
            print("Tasks are completed")
    # run_task()