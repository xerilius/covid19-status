"""Parse data from API and store into database"""

from datetime import datetime
# make json file more readable
import json
# Needed to make API Requests, threading, etec
import requests, os, bs4, threading, time

from model import connect_to_db, db, Status, City, State_

# No API key needed
URL = "https://api.covid19api.com/country/us/status/confirmed"
URL2 = "https://api.covid19api.com/country/us/status/deaths"

def create_status():
    """Organize data before transferring into db"""

    # Retrieve data thru json file
    with open('confirmed.json', 'r') as outfile:
        api_data = json.load(outfile)

    status_data = {
        'state': None,
        'city': "None",
        'confirmed': None,
        'date': None,
    }

    states_ = {}
    cities_ = {}
    db_cities = {}

    for dict_ in api_data:
        state = dict_['Province']
        states_[state] = state

        city = dict_.get('City', "None")
        cities_[city] =  state

    # Adding all states
    for key in states_.keys():
        usa_states = State_(state_name = key)
        db.session.add(usa_states)
        db.session.commit()

    # Adding all cities
    for key in cities_.keys():
        db_cities[key] = City(city_name = key)
  
   ########################################## 

    for dict_ in api_data:
        city = dict_.get('City', "None")
        status_data['city'] = city

        case = dict_['Cases']
        status_data['case'] = case

        date = dict_['Date']
        date = datetime.strptime(date[0:10], '%Y-%m-%d')
        status_data['date'] = date

        status = Status(
            confirmed=int(status_data['case']),
            status_date=status_data['date'],
        )
        
    
        ree = db_cities[city]
        reee = status.city_status.append(ree)

        db.session.add(status)
        db.session.commit()


    # for dict_ in dicts:
    #     state = dict_['Province']
    #     status_data['state'] = state
    #     states_[state] = state
        
    #     city = dict_.get('City',"None")
    #     status_data['city'] = city
    #     cities_[city] =  city

    #     case = dict_['Cases']
    #     status_data['case'] = case

    #     date = dict_['Date']
    #     date = datetime.strptime(date[0:10], '%Y-%m-%d')
    #     status_data['date'] = date
        
    
        # status = Status(
        #     confirmed=int(status_data['case']),
        #     status_date=status_data['date'],
        # )
        # status.city_status.append(City(city_name=status_data['city']))
        # usa_states = State_(state_name = states_[state])
        # db.session.add(status) 
        # db.session.commit()




        # AttributeError: 'State_' object has no attribute 'status'
            # usa_states.status.append(State_(state_name=status_data['state']))

  
    # usa_states = State_(state_name = states_[state])
    # usa_states.cities.append(City(city_name=cities_[city]))
    # db.session.add(usa_states)
    # db.session.commit()


    # print(f'Created {status}')


def write_confirmed_data():
    """Writes confirmed/death reports of COVID-19 in each state to txt file."""
    r1 = requests.get(URL)
    # # Method 1
    # with open('confirmed-reports.txt', 'w') as f:
    #     f.write(r1.text)

    # Method 2
    data_ = json.loads(r1.text)
    with open('confirmed-reports.json', 'w') as outfile:
        json.dump(data_, outfile, indent=4)
    print('task done')


def write_death_data(json):
    r2 = requests.get(URL2)
    with open('deaths-reports.txt', 'w') as f:
        f.write(r2.text)

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
    # Make tables
    db.create_all()

    # Enter data into DB
    create_status()



    # def run_task():
    #     """Run task 7 times"""
    #     for i in range(0,1):
    #         t1 = threading.Thread(target=get_confirmed_status, args=(confirmed_txt,))
    #         t2 = threading.Thread(target=get_death_status, args=(deaths_txt,))
    #         # start thread 
    #         t1.start()
    #         print("t1 started")
    #         t2.start()
    #         print("t2 started")

    #         # time.sleep(1440)   
    #         # wait until threads are completely executed
    #         t1.join()
    #         t2.join()
    #         # both threads are completely executed
    #         print("Tasks are completed")
    # run_task()


####################################   
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
            