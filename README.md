<h1 align="center">  𝘾𝙊𝙑𝙄𝘿⑲𝙎𝙏𝘼𝙏𝙐𝙎  </h1>
Covid19 Status is a Python/Flask app that allows users to search up confirmed cases of Covid19 in their county.
<br>  
A graph made with D3 shows the stats for the past 10 days.  

<br>

Features soon to be implemented include stats on fatalities and a tracker button that allows users to follow trends,
which will be displayed in the user dashboard.
<br>
<br>

<b><ins>BUILT WITH</ins></b>  
<a href="https://docs.python.org/3/">
<img src="https://icongr.am/devicon/python-original.svg?size=50"></a>
<a href="https://d3js.org/">
<img src="https://icongr.am/devicon/d3js-original.svg?size=50"></a>
<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript">
  <img alt="js" src="https://icongr.am/devicon/javascript-original.svg?size=50"></a> 
<a href="https://jquery.com/">
<img src="https://icongr.am/devicon/jquery-original.svg?size=50"></a>
<a href="https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5">
  <img alt="html" src="https://icongr.am/devicon/html5-original-wordmark.svg?size=60"></a>
<a href="https://developer.mozilla.org/en-US/docs/Web/CSS">
  <img alt="css" src="https://icongr.am/devicon/css3-original-wordmark.svg?size=60"></a>
<a href="https://sass-lang.com/documentation">
<img src="https://icongr.am/devicon/sass-original.svg?size=50"></a>
<a href="https://www.postgresql.org/about/">
<img src="https://icongr.am/devicon/postgresql-original.svg?size=50"></a>
<a href="https://flask.palletsprojects.com/en/1.1.x/">
<img src="https://icongr.am/simple/flask.svg?size=50"></a>

<b><ins>OTHER TECHNOLOGIES</ins></b>  
 SQLAlchemy & Jinja2  

<b><ins>API</ins></b>  
COVID19API  

<br>

![Projectl](./static/img/covid-status.gif)

<b><ins>DATABASE TABLES</ins></b>  
User | Data Type | Keys 
:--: | :--: | :--: 
user_id | Integer | primary_key
username | String | - 
signup_date | Date | - 

<br>

County | Data Type | Keys 
:--: | :--: | :--: 
county_id | Integer | primary_key
county_name | String | -
state_name | String | -

<br>

Case | Data Type | Keys 
:--: | :--: | :--: 
case_id | Integer | primary_key
case_date | Date | - 
county_id | Integer | foreign_key
state_name| String | -
confirmed | Integer | - 
deaths | Integer | -
recovered | Integer | - 
active | Integer |

<br>

Save | Data Type | Keys
:--: | :--: |:--:
user_id | Integer | foreign_key
city_id | Integer | foreign_key


<br>

<!-- <b><ins>DATA MODEL</ins></b>    -->

<!-- ![Data Model](./static/img/datamodel.png) -->

<br>

## INSTALLATION

#### Clone or fork this repo:

$ `git clone https://github.com/xerilius/covid19-status.git`


#### Create & Activate Virtual Environment
$ `virtualenv env`  
$ `source env/bin/activate`


#### Install dependencies
(env) $ `pip3 install -r requirements.txt`

#### Seed data into database
(env) $ `python3 seed.py`  
<sub>**Note:** Will take a while to insert all data into the database</sub>  
<sub>You can update the data daily by  uncommenting `run_task()` at the bottom of the file
</sub>


#### Start Flask Server
(env) $ `export FLASK_APP=server.py`  
(env) $ `flask run --host=0.0.0.0`

#### Go to http://localhost:5000/ in your browser