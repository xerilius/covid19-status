# COVID 19 TRACKER

#### Go to project directory

#### Create & Activate Virtual Environment
$ `virtualenv env`  
$ `source env/bin/activate`


#### Install dependencies
$ `pip3 install -r requirements.txt`



#### Start Flask Server
$ `export FLASK_APP=server.py`  
$ `flask run --host=0.0.0.0`

<br>

#### Seed data into database
$ `python3 seed.py`  
<sub>**Note:** Will take a while to insert all data into the database</sub>