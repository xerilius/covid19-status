"""Parse data from API and store into database"""

from datetime import datetime
from model import connect_to_db, db, County, Fatality, Confirmed
import requests, os, bs4, threading, time
import json


# No API key needed
URL = "https://api.covid19api.com/country/us/status/confirmed"
URL2 = "https://api.covid19api.com/country/us/status/deaths"
USTOTALSTATS = "https://api.covid19api.com/total/country/us"


def seed_data_directly_from_api():
    """Parsing JSON directly from API response and seed into database."""

    confirmed_response = requests.get(URL)
    fatality_response = requests.get(URL2)

    dataset_confirmed = json.loads(confirmed_response.text)
    dataset_fatality = json.loads(fatality_response.text)

    status_data = {
        'state': None,
        'city': None,
        'confirmed': None,
        'date': None,
        'city_id': None,
        'lat': None,
        'lon': None,
    }

    city_seen = {}
    db_cities = {"Unassigned": 0}
    i = 1
    # Creating county_ids & inserting data into County Table
    for dict_ in dataset_confirmed:  
        if dict_['City']:
            city = dict_['City']
            status_data['city'] = city

        state = dict_['Province']
        status_data['state'] = state


        lat = dict_['Lat']
        status_data['lat'] = lat

        lon = dict_['Lon']
        status_data['lon'] = lon

        if status_data['city'] not in city_seen:
            if status_data['city'] == "Unassigned":
                i += 0
            else: 
                county = County(county_name = status_data['city'], 
                                    state_name=status_data['state'],
                                    lat=status_data['lat'],
                                    lon=status_data['lon']
                                    )
                city_seen[status_data['city']] = status_data['city']
                db_cities[status_data['city']] = i 
                i += 1
            db.session.add(county)       
        db.session.commit()     
    print(f"Successfully created {county}")


    city_seen = {} 

    # Create Status Table
    for dict_ in dataset_confirmed:
        if dict_['City']:
            city = dict_['City']
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

        confirmed = Confirmed(
            confirmed=int(status_data['case']),
            date=status_data['date'],
            county_id=int(status_data['city_id']),
            state_name=status_data['state']
        )
        db.session.add(confirmed)
    db.session.commit()
    print(f"Successfully created {confirmed}")


    city_seen = {}
    # Insert data into Fatality Table
    for dict_ in dataset_fatality:
        if dict_['City']:
            city = dict_['City']
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

        fatality = Fatality(
            fatalities=int(status_data['case']),
            date=status_data['date'],
            county_id=int(status_data['city_id']),
            state_name=status_data['state']
        )
        db.session.add(fatality)
    db.session.commit()
    print(f"Successfully created {fatality}")


#############################################################

def read_json():
    """Reads json file"""

    with open('confirmed-reports.json', 'r') as outfile:
        api_data = json.load(outfile)
    return api_data


def create_county_ids():
    """Returns dictionary of county_ids"""

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


def run_all_json_files():
    """Reads all JSON files"""
    enter_county_data()
    enter_confirmed_data()
  

def enter_county_data():
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
                county_inst = County(county_id=db_cities[status_data['city']],
                                county_name=status_data['city'],
                                state_name=status_data['state']
                                )
                db.session.add(county_inst)
            city_seen[status_data['city']] = db_cities[status_data['city']]
    db.session.commit()

                  
def enter_confirmed_data():
    """Inserts data for the confirmed status table"""

    api_data = read_json()
    db_cities = create_city_ids()

    status_data = {
        'state': None,
        'city': None,
        'confirmed': None,
        'date': None,
        'city_id': None,
    }

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
            county_id=int(status_data['city_id']),
            state_name=status_data['state']
        )
        db.session.add(status)
    db.session.commit()

    print(f"Successfully created {status}")

    
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

    # # Method 3
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
    
    db.session.add(
        County(county_id=0, 
            county_name="Unassigned", 
            state_name="TBA",
            lat=0,
            lon=0))
    db.session.commit()

    # seed_data_directly_from_api()
    # run_all_json_files()
    

