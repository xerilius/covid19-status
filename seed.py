"""Parse data from API and store into database"""

from datetime import datetime
from model import connect_to_db, db, Status, City
import requests, os, bs4, threading, time
import json

# No API key needed
URL = "https://api.covid19api.com/country/us/status/confirmed"
URL2 = "https://api.covid19api.com/country/us/status/deaths"


def read_json():
    """Reads json file"""

    with open('confirmed-reports.json', 'r') as outfile:
        api_data = json.load(outfile)

    return api_data


def create_city_ids():
    """Returns dictionary of city_ids"""

    api_data = read_json()
    
    status_data = {
        'city': None,
        'city_id': 0,
    }
    city_seen = {}
    db_cities = {'Unassigned': 0}
    i = 1

    for dict_ in api_data:
        city = dict_.get("City")
        status_data['city'] = city

        if status_data['city'] not in city_seen:
            if status_data['city'] == 'Unassigned':
                i += 0
            else: 
                city_seen[status_data['city']] = status_data['city']
                db_cities[status_data['city']] = i 
                i += 1

    return db_cities
    

def enter_city_data():
    """Inserts data for the City table"""
    api_data = read_json()
    db_cities = create_city_ids()

    status_data = {
        'state': None,
        'city': None,
        'city_id': None,
    }
    city_seen = {}

    for dict_ in api_data:
        city = dict_.get('City')
        status_data['city'] = city

        state = dict_['Province']
        status_data['state'] = state

        if status_data['city'] not in city_seen:
            if status_data['city'] != "Unassigned":
                city_inst = City(city_id=db_cities[status_data['city']],
                                city_name=status_data['city'],
                                state_name=status_data['state']
                                )
                db.session.add(city_inst)
            city_seen[status_data['city']] = db_cities[status_data['city']]
    db.session.commit()

                  
# def enter_confirmed_data():
#     """Inserts data for the confirmed status table"""

#     api_data = read_json()
#     db_cities = create_city_ids()

#     status_data = {
#         'state': None,
#         'city': None,
#         'confirmed': None,
#         'date': None,
#         'city_id': None,
#     }

#     city_seen = {}

#     # Create Status Table
#     for dict_ in api_data:
#         city = dict_.get('City', "None")
#         status_data['city'] = city
#         if city in db_cities:
#             status_data['city_id'] = db_cities[city]

#         state = dict_['Province']
#         status_data['state'] = state

#         case = dict_['Cases']
#         status_data['case'] = case

#         date = dict_['Date']
#         date = datetime.strptime(date[0:10], '%Y-%m-%d')
#         status_data['date'] = date

#         status = Status(
#             confirmed=int(status_data['case']),
#             status_date=status_data['date'],
#             city_id=int(status_data['city_id']),
#             state_name=status_data['state']
#         )
#         db.session.add(status)
#         db.session.commit()

#     # print(f"Successfully created {status}")



def run_writing_tasks():
    """Update and rewrite data from API"""
    for i in range(0, 1):
        t1 = threading.Thread(target=write_confirmed_data)
        t2 = threading.Thread(target=write_fatality_data)

        t1.start()
        print("Task#1 started")
        t2.start()
        print("Task#2 started")

        # time.sleep(1440) 

        # wait until threads are completely executed
        t1.join()
        t2.join()

        print("All tasks are completed")



def write_confirmed_data():
    """Writes confirmed reports of COVID-19 in each state to jsonile."""
    r1 = requests.get(URL)
    confirmed_data = json.loads(r1.text)
    with open('confirmed-reports.json', 'w') as outfile:
        json.dump(confirmed_data, outfile, indent=4)
    print('Task#1 completed.')



def write_fatality_data():
    """Writes fatality reports of COVID-19 in each state to jsonfile."""
    r2 = requests.get(URL2)
    fatality_data = json.loads(r2.text)

    with open('fatality-reports.json', 'w') as outfile:
        json.dump(fatality_data, outfile, indent=4)
    print('Task#2 completed.')

    # # Method 2
    # with open('fatality-reports.json', 'w') as outfile:
    #     outfile.write(r2.text)
    # print('Task#2 completed.')

    # # Method 3
    # fatality_data = json.loads(r2.text)
    # out_file = open(json, "w")
    # json.dump(fatality_data, out_file, indent=4)
    # out_file.close()


if __name__ == "__main__":
    from server import app
    import os

    # run_writing_tasks()

    os.system("dropdb covid19")
    os.system("createdb covid19")

    connect_to_db(app)
    db.create_all()
    
    db.session.add(City(city_id=0, city_name="Unassigned", state_name="TBD"))
    db.session.commit()
    enter_city_data()
    # enter_table_data()

    


# # To seed data directly into DB without saving data into a file 
    # response = requests.get(URL)
    # response.raise_for_status()
    # data_= json.loads(response.text)
    # w = data_
