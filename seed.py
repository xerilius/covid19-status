"""Parse data from API and store into database"""
import json
import requests, os, bs4, threading, time
from datetime import datetime
from model import connect_to_db, db, County, Case, Usa


# No API key needed

URL = "https://api.covid19api.com/country/us?from=2020-01-22T00:00:00Z&to=2020-03-22T00:00:00Z"

URL3 = "https://api.covid19api.com/total/country/us"

start_date = "2020-05-17"
end_date = "2020-05-20"
URL_UPDATE_DATA = f"https://api.covid19api.com/country/us?from={start_date}T00:00:00Z&to={end_date}T00:00:00Z"


def create_county_ids():
    """Returns dictionary with county_name, state_name and ids"""
    api_data = requests.get(URL)
    dataset = json.loads(api_data.text)

    status_data = { 
    'state': None,
    'city': None,
    'city_id': None,  
    }

    city_seen = {}
    db_cities = {}
    i = 1

    for dict_ in dataset:  
        if dict_['City']:
            city = dict_['City']
            
        if dict_['Province']:
            state = dict_['Province']
            status_data['state'] = state
            status_data['city'] = city + "," + " " + state

        if status_data['city'] not in city_seen:
            city_seen[status_data['city']] = status_data['city']
            db_cities[status_data['city']] = i 
            i += 1

    # write db_cities dict into a json file
    json_file = json.dumps(db_cities)
    f = open("db_cities.json", "w")
    f.write(json_file)
    f.close()

    print("File: db_cities.json successfully created")
    


def update_data_from_api_response(db_cities):
    update_data = requests.get(URL_UPDATE_DATA)
    # dumps --> takes in Python obj and convert it to string
    # loads --> Take JSON string and convert to Python obj
    dataset_update = json.loads(update_data.text)

    status_data = {
        'state': None,
        'city': None,
        'confirmed': None,
        'deaths': None,
        'recovered': None,
        'active': None,
        'date': None,
        'city_id': None,   
    }

    for dict_ in dataset_update:
        city = dict_['City']
          
        state = dict_['Province']
        status_data['state'] = state
        status_data['city'] = city + "," + " " + state

        if (city + "," + " " + state) in db_cities:
            status_data['city_id'] = db_cities[city + "," + " " + state]

        confirmed = dict_['Confirmed']
        status_data['confirmed'] = confirmed

        deaths = dict_['Deaths']
        status_data['deaths'] = deaths

        recovered = dict_['Recovered']
        status_data['recovered'] = recovered

        active = dict_['Active']
        status_data['active'] = active

        date = dict_['Date']
        date = datetime.strptime(date[0:10], '%Y-%m-%d')
        status_data['date'] = date

        cases = Case(
            confirmed=status_data['confirmed'],
            deaths=status_data['deaths'],
            recovered=status_data['recovered'],
            active=status_data['active'],
            date=status_data['date'],
            county_id=status_data['city_id'],
            state_name=status_data['state']
        )

        db.session.add(cases)
    db.session.commit()
    print(f"Successfully created {cases}")

##############################################################################

def read_db_cities_json():
    """Reads db_cities.json to create db_cities dict for county names"""

    with open('db_cities.json', 'r') as outfile:
        db_cities = json.load(outfile)

    return db_cities


def insert_county_data(db_cities):
    """Parsing JSON directly from API response and seed into database."""

    confirmed_response = requests.get(URL)
    dataset_confirmed = json.loads(confirmed_response.text)

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

    # Creating county_ids & inserting data into County Table
    for dict_ in dataset_confirmed:  
        if dict_['City']:
            city = dict_['City']
            
        if dict_['Province']:
            state = dict_['Province']
            status_data['state'] = state
            status_data['city'] = city + "," + " " + state

        if dict_['Lat']:
            lat = dict_['Lat']
            status_data['lat'] = lat

        if dict_['Lon']:
            lon = dict_['Lon']
            status_data['lon'] = lon

        if status_data['city'] not in city_seen:
            db_county = status_data['city'].split(",")
            db_county_name = db_county[0]
            county = County(county_name = db_county_name, 
                                state_name=status_data['state'],
                                lat=status_data['lat'],
                                lon=status_data['lon']
                                )
            city_seen[status_data['city']] = status_data['city']
            db.session.add(county)
    db.session.commit()   
    print(f"Successfully created {county}")



def seed_usa_total_data_from_api():
    """Inserting total stats in US - confirmed, fatalities, recovered"""

    usa_total_response = requests.get(URL3)
    dataset_usa_total = json.loads(usa_total_response.text)

    status_data = {
        'confirmed': None,
        'deaths': None,
        'date': None,
        'recovered': None,
    }

    for dict_ in dataset_usa_total:

        confirmed = dict_['Confirmed']
        status_data['confirmed'] = confirmed
              
        deaths = dict_['Deaths']
        status_data['deaths'] = deaths

        # recovered = dict_['Recovered']
        # status_data['recovered'] = recovered

        date = dict_['Date']
        date = datetime.strptime(date[0:10], '%Y-%m-%d')
        status_data['date'] = date

        usa_total = Usa(
            confirmed_total=status_data['confirmed'],
            fatality_total=status_data['deaths'],
            date=status_data['date']
        )
        print(usa_total)
        db.session.add(usa_total)
    db.session.commit()

    print(f"Successfully created {usa_total}")




if __name__ == "__main__":
    from server import app
    import os

    # os.system("dropdb covid19")
    # os.system("createdb covid19")

    connect_to_db(app)
    db.create_all()

    db_cities = read_db_cities_json()
    # insert_county_data(create_county_ids())
    # update_data_from_api_response(db_cities)
    db.session.query(Usa).delete()
    db.session.commit()
    seed_usa_total_data_from_api()

