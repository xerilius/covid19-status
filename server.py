from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import asc, desc
from model import connect_to_db, db, County, Fatality, Confirmed, User, Usa, Save

import json
from datetime import date, datetime

app = Flask(__name__)
# # set a 'SECRET_KEY' to enable the Flask session cookies
# app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.secret_key = "abc"  # will always store key in secrets.sh file or .env

app.jinja_env.undefined = StrictUndefined


# SAVE BUTTON
@app.route('/save/<county_id>', methods=["POST"])
def create_save(county_id):
    """Create save for county"""
    username = session['username']
    user = User.query.filter_by(username=username).first()
    user_id = user.user_id
    

    get_county = db.session.query(County).filter(County.county_id==int(county_id)).first()
    county_id = get_county.county_id

    # check save
    if request.method == 'POST':
        check_save_exists = db.session.query(Save).filter(Save.user_id==user_id, Save.county_id==county_id).first()

        if check_save_exists:
            return ("Already Saved")

        elif check_save_exists == None:
            save_data = Save(user_id=int(user_id), county_id=int(county_id))
            db.session.add(save_data)
            db.session.commit()
            print(">>>>> SAVED <<<<<", save_data)
            
    return (">>> OK <<<", 200)


def get_username():
    """Get username from session"""

    username = session['username']
    user = User.query.filter_by(username=username).first()
    user_id = user.user_id

    return user_id


def get_countystate_from_slug(county_info):    
    save_info = county_info.split("-")
    state_name = save_info[-1]
    county_info = save_info[:-1]
    county_name = " ".join(county_info)

    return [county_name, state_name]
    

# UNSAVE 
@app.route('/delete/<county_id>', methods=["POST"])
def delete_save(county_id):
    """Unsave county"""
    username = session['username']
    user = User.query.filter_by(username=username).first()
    user_id = user.user_id


    get_county = db.session.query(County).filter(County.county_id==county_id).first()
    county_id = get_county.county_id

    get_save = db.session.query(Save).filter(Save.county_id==county_id, Save.user_id==user_id).first()
    save_id = get_save.save_id

    print(">>>>> DELETE <<<<<", Save.query.get(int(save_id)))

    db.session.delete(Save.query.get(int(save_id)))
    db.session.commit()
    
    return (">>> UNSAVED <<<", 200)


# SEARCH RESULTS
@app.route('/search-results', methods=["POST"])
def show_results():
    """Displays city from search result"""

    county_search = request.form.get("searchbar")
    print(county_search)
    search = "%{}%".format(county_search).title().strip()
    county_data = County.query.filter(County.county_name.ilike(search)).all()

    if len(county_data) == 1: 
        for county_inst in county_data:     
            county_id = county_inst.county_id

            confirmed10 = db.session.query(Confirmed).filter(Confirmed.county_id == county_id).order_by(desc(Confirmed.confirmed_id)).limit(10)
                
            # Check Saves for User
            if 'username' in session:
                username = session['username']
                user = User.query.filter_by(username=username).first()
                user_id = user.user_id
                
                saved = db.session.query(Save).filter(Save.county_id==county_id, Save.user_id==user_id).first()
            else:
                saved = None
                user_id= None
        
            # D3 Graph 
            datasets = []
            for item in confirmed10:
                datasets.append({
                    'date': str(item.date), 
                    'num': item.confirmed
                })
                data = json.dumps({"data":datasets})

        return render_template('/county-info.html', 
                            counties=county_inst, 
                            confirmed10=confirmed10, 
                            data=data, 
                            saved=saved, 
                            user_id=user_id)

    
    return render_template('search-results.html', counties=county_data)



@app.route('/county/<county_id>', methods=["GET"])
def show_county_info(county_id):
    """Displays county information"""

    county_inst = County.query.filter(County.county_id==int(county_id)).first()
    
    state_name = county_inst.state_name
    county_id = county_inst.county_id

    # Get Recent 10 Records 
    confirmed10 = db.session.query(Confirmed).filter(Confirmed.county_id == county_id).order_by(desc(Confirmed.confirmed_id)).limit(10)

    # Check Saves for User
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        user_id = user.user_id
        
        saved = db.session.query(Save).filter(Save.county_id==county_id, Save.user_id==user_id).first()
    else:
        saved = None
        user_id= None
  
    # D3 Graph 
    datasets = []
    for item in confirmed10:
        datasets.append({
            'date': str(item.date), 
            'num': item.confirmed
        })

        data = json.dumps({"data":datasets})

    return render_template('county-info.html', 
                            counties=county_inst, 
                            states=state_name, 
                            confirmed10=confirmed10, 
                            data=data, saved=saved, user_id=user_id)

# DASHBOARD
@app.route('/user/<username>', methods=["GET"])
def show_dashboard(username):
    """Displays user to Dashboard"""

    today = datetime.now()
    current_date = today.strftime("%B %d, %Y")

    username = session.get("username")
    if username:
        user = db.session.query(User).filter(User.username==username).first()
        user_name = user.username
        user_id = user.user_id

    # query for all saves ids with user_id # to display on dashboard side nav 
    county_id_list = []
    saves = db.session.query(Save).filter(Save.user_id==user_id).all()
    for county in saves:
        county_id = county.county_id
        county_id_list.append(county_id)
    print("@@@@@@@@@@@@",county_id_list)
    county_inst_list = []
    for id in county_id_list:
        # get name of each county & state with id#
        county_inst = db.session.query(County).filter(County.county_id==id).first()
        county_name = county_inst.county_name
        state_name = county_inst.state_name
        county_state = county_name + ", " + state_name
        county_inst_list.append(county_state)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", county_inst_list)
    # county_id_list.clear()

    return render_template("dashboard.html", 
                                current_date=current_date,
                                username=user_name, saves=saves, county_list=county_inst_list)


# HOMEPAGE
@app.route('/', methods=["GET"])
def index():
    """Homepage"""

    country_total= db.session.query(Usa.confirmed_total, Usa.fatality_total).order_by(desc(Usa.date)).limit(1)

    for item in country_total:
        confirmed_total = item[0]
        fatality_total = item[1]
    
    return render_template("index.html", 
                        confirmed_total=confirmed_total, 
                        fatality_total=fatality_total)


# SIGNUP
@app.route('/signup', methods=["GET"])
def show_signup_form():
    """Displays signup form"""

    return render_template("signup.html")


@app.route('/signup', methods=["POST"])
def process_signup():
    """Stores user registration data in db, redirect to homepage"""

    username = request.form.get('username').lower()
    email =  request.form.get('email')
    pw = request.form.get('pwd')

    # Validate/Check Username in DB
    if User.query.filter(User.username == username).first():
        flash("Username already exists.")
        return redirect('/signup')
    # Check Email in DB
    if User.query.filter(User.email == email).first():
        flash("Email already exists")
        return redirect('/signup')
    else:
        current_date = date.today()
        signup_date = current_date.strftime("%Y-%b-%d")
        # Store username & pw in DB
        db.session.add(User(username=username, 
                            email=email.lower(),
                            pw=pw,
                            signup_date=signup_date))
        db.session.commit()

    return redirect('/')


# LOGIN
@app.route('/login', methods=["GET"])
def show_login_form():
    """Displays login form"""

    return render_template("login.html")


@app.route('/login', methods=["POST"])
def process_login():
    """Queries database, redirects to dashboard"""

    username = request.form.get("username")
    pw = request.form.get("pwd")
    username = username.lower()
    user = User.query.filter_by(username=username, pw=pw).first()
    if not user:
        flash("Invalid Username or Password.")
        return redirect('/login')
    
    session['username'] = user.username

    return redirect('/')


# LOGOUT
@app.route('/logout')
def logout():
    """Logout user"""

    del session['username']
    flash("You successfully logged out")
    return redirect('/')




if __name__ == '__main__':
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(debug=True, host='0.0.0.0')