# COVID 19 TRACKER

#### <ins>Go to project directory</ins> 

#### <ins>Create & Activate Virtual Environment</ins>
$ `virtualenv env`  
$ `source env/bin/activate`

<br>

#### </ins>Install dependencies </ins>
$ `pip3 install -r requirements.txt`

<br>

#### <ins>Start Flask Server </ins>
$ `export FLASK_APP=server.py`  
$ `flask run --host=0.0.0.0`

<br>

#### <ins>Seed data into database</ins>
$ `python3 seed.py`  
<sub>**Note:** Will take a while to insert all data into the database</sub>