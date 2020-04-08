"""Parse data from API and store into database"""

from datetime import datetime
from model import connect_to_db, db, Status, City
import requests, os, bs4, threading, time
import json

# No API key needed
URL = "https://api.covid19api.com/country/us/status/confirmed"
URL2 = "https://api.covid19api.com/country/us/status/deaths"

def create_city_table():
    

    with open('confirmed.json', 'r') as outfile:
        api_data = json.load(outfile)

    db_cities = {}

    status_data = {
        'state': None,
        'city': "None",
        'confirmed': None,
        'date': None,
    }

    city_seen = {}



def enter_table_data():
    # Retrieve data thru json file
    with open('confirmed.json', 'r') as outfile:
        api_data = json.load(outfile)

    status_data = {
        'state': None,
        'city': "None",
        'confirmed': None,
        'date': None,
        'city_id': None,
    }

    city_seen = {}
    db_cities = {"Unassigned": 0}
    i = 1

    # Create City Table & Manually creating city_ids
    for dict_ in api_data:
        city = dict_.get('City', "None")
        status_data['city'] = city

        state = dict_['Province']
        status_data['state'] = state

        if status_data['city'] not in city_seen:
            if status_data['city'] == "Unassigned":
                i += 0
            else: 
                city_inst = City(city_name = status_data['city'], 
                                    state_name=status_data['state'])
                city_seen[status_data['city']] = status_data['city']
                db_cities[status_data['city']] = i 
                i += 1
            db.session.add(city_inst)       
        db.session.commit()
     
    print(f"Successfully created {city_inst}")
    print(db_cities)

    city_seen = {} 

    # Create Status Table
    for dict_ in api_data:
        city = dict_.get('City', "None")
        status_data['city'] = city
        if city in db_cities:
            status_data['city_id'] = db_cities[city]

        state = dict_['Province']
        status_data['state'] = state

        case = dict_['Cases']
        status_data['case'] = case

        date = dict_['Date']
        date = datetime.strptime(date[0:10], '%Y-%m-%d')
        status_data['date'] = date

        status = Status(
            confirmed=int(status_data['case']),
            status_date=status_data['date'],
            city_id=int(status_data['city_id']),
            state_name=status_data['state']
        )
        db.session.add(status)
        db.session.commit()

    print(f"Successfully created {status} and {city_inst}")


def write_confirmed_data():
    """Writes confirmed reports of COVID-19 in each state to txt file."""
    r1 = requests.get(URL)
    data_ = json.loads(r1.text)
    with open('confirmed-reports.json', 'w') as outfile:
        json.dump(data_, outfile, indent=4)
    print('Task#1 completed.')

    # # Method 2
    # with open('confirmed-reports.txt', 'w') as f:
    #     f.write(r1.text)


def write_death_data(json):
    """Writes death reports of COVID-19 in each state to txtfile."""
    r2 = requests.get(URL2)
    with open('deaths-reports.json', 'w') as outfile:
        outfile.write(r2.text)
    print('Task#2 completed.')

    # # Method 2
    # deaths_data = json.loads(r2.text)
    # out_file = open(json, "w")
    # json.dump(deaths_data, out_file, indent=4)
    # out_file.close()



if __name__ == "__main__":
    from server import app
    import os

    os.system("dropdb covid19")
    os.system("createdb covid19")

    connect_to_db(app)
    db.create_all()

    db.session.add(City(city_id=0, city_name="Unassigned"))
    db.session.commit()
    enter_table_data()
    # enter_table_data()


    def run_task():
        """Update and rewrite data from API"""
        for i in range(0,1):
            t1 = threading.Thread(target=get_confirmed_status)
            t2 = threading.Thread(target=get_death_status)
    
            t1.start()
            print("t1 started")
            t2.start()
            print("t2 started")

            # time.sleep(1440) 

            # wait until threads are completely executed
            t1.join()
            t2.join()

            print("All tasks are completed")
    # run_task()


# # To seed data directly into DB without saving data into a file 
    # response = requests.get(URL)
    # response.raise_for_status()
    # data_= json.loads(response.text)
    # w = data_

    # for dictionaries in w:
    #     # dictionaries = all dictionaries in the list

    #     for key in dictionaries:
    #         states = dictionaries.get("Province")
    #         api_data['state'] = states
    #         states_[states] = states

    #         cities = dictionaries.get("City")
    #         api_data['city'] = cities
    #         # cities_[cities]=states
    #         cities_[cities]=cities

    #         cases = dictionaries.get("Cases")
    #         api_data['cases'] = cases

    #         date = dictionaries.get("Date")
    #         api_data['date'] = date
            