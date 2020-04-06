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
        dicts = json.load(outfile)

    api_data = {
        'state': None,
        'city': None,
        'confirmed': None;
        'date': None;
    }

    # create values for api_data dictionary
    for dict_ in dicts:
        state = dict_.get('Province')
        api_data['state'] = state
        
    # Note: cities = dict_['City'] results in a KeyError
        city = dict_.get('City',"None")
        api_data['city'] = city
        cities_[city] =  city

        case = dict_.get('Cases')
        api_data['case'] = case

        date = dict_.get('Date')
        date = datetime.strptime(date[0:10], '%Y-%m-%d')
        api_data['date'] = date
        
        status = Status(
            confirmed=int(api_data['case']),
            status_date=api_data['date'],
        )
    db.session.add(status)
    state_class = State(
        state_name = states_[state]
    )
    for key2 in cities_:
        
            status.city_id.append(city.city_name=key2)

    db.session.add(status) 
    db.session.commit()
    print(f'Created {status}')



    ca = State_(state_name = "California")
    ca.cities.append(City(city_name="San Francisco"))
    db.session.add(ca)
    db.session.commit()





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
    # connect and create db
    connect_to_db(app)
    db.create_all()

    # Enter data into DB
    create_status()



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
            