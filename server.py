from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

app = Flask(__name__)


app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""
    return render_template("index.html")


# SIGNUP
@app.route('/signup', methods=["GET"])
def show_signup_form():
    """Displays signup form"""
    return render_template("signup.html")

@app.route('/signup', methods=["POST"])
def process_signup():
    """Stores user registration data in db, redirect to homepage"""
    return redirect('/')


# LOGIN
@app.route('/login', methods=["GET"])
def show_login_form():
    """Displays login form"""
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def process_login():
    """Queries database, redirects to dashboard"""
    return redirect('/user')


# DASHBOARD
@app.route('/user')
def user_login():
    """Redirects user to Dashboard"""
    return render_template("dashboard.html")
    

if __name__ == '__main__':
    # connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(debug=True, host='0.0.0.0')

