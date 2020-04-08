<h1 align="center"> COVID-19 TRACKER </h1>

<b><ins>BUILT WITH</ins></b>  
<a href="#">
<img src="https://icongr.am/devicon/python-original.svg?size=50"></a>
<a href="#">
<img src="https://icongr.am/devicon/d3js-original.svg?size=50"></a>
<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript">
  <img alt="js" src="https://icongr.am/devicon/javascript-original.svg?size=50"></a> 
<a href="#">
<img src="https://icongr.am/devicon/jquery-original.svg?size=50"></a>
<a href="https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5">
  <img alt="html" src="https://icongr.am/devicon/html5-original-wordmark.svg?size=60"></a>
<a href="https://developer.mozilla.org/en-US/docs/Web/CSS">
  <img alt="css" src="https://icongr.am/devicon/css3-original-wordmark.svg?size=60"></a>
<a href="https://sass-lang.com/documentation">
<img src="https://icongr.am/devicon/sass-original.svg?size=50"></a>
<a href="#">
<img src="https://icongr.am/devicon/postgresql-original.svg?size=50"></a>
<a href="#">
<img src="https://icongr.am/devicon/vagrant-original.svg?size=50"></a>
<a href="#">
<img src="https://icongr.am/simple/flask.svg?size=50"></a>

<b><ins>OTHER TECHNOLOGIES</ins></b>  
 SQLAlchemy & Jinja2  

<b><ins>API</ins></b>  
<a href="https://covid19api.com/#details">COVID-19 API</a>   

<br>


<b><ins>DATABASE TABLES</ins></b>  
User | Data Type | Keys 
:--: | :--: | :--: 
user_id | Integer | primary_key
username | String | - 
signup_date | Date | - 

<br>

City | Data Type | Keys 
:--: | :--: | :--: 
city_id | Integer | primary_key
city_name | String | -
state_name | String | -

<br>

Status | Data Type | Keys 
:--: | :--: | :--: 
status_id | Integer | primary_key
status_date | Date | - 
city_id | Integer | foreign_key
state_name| String | -
confirmed | Integer | - 

<br>

<b><ins>DATA MODEL</ins></b>  
![Data Model](./static/img/datamodel.png)

<br>

## INSTALLATION

#### Go to project directory

#### Create & Activate Virtual Environment
$ `virtualenv env`  
$ `source env/bin/activate`


#### Install dependencies
(env) $ `pip3 install -r requirements.txt`

#### Seed data into database
(env) $ `python3 seed.py`  
<sub>**Note:** Will take a while to insert all data into the database</sub>

#### Start Flask Server
(env) $ `export FLASK_APP=server.py`  
(env) $ `flask run --host=0.0.0.0`

#### Go to http://localhost:5000/ in your browser

