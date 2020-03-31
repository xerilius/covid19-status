from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

app = Flask(__name__)


app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""
    return render_template("index.html")


@app.route('/signup', methods=["GET"])
def show_signup_form():
    """Displays signup form"""
    return render_template("signup-form.html")

@app.route('/signup', methods=["POST"])
def process_signup():
    """Stores user registration data in db, redirect to homepage"""
    return redirect('/')


@app.route('/user')
def user_login():
    """Redirects user to Dashboard"""
    return render_template("dashboard.html")
    

if __name__ == '__main__':
    # connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(debug=True, host='0.0.0.0')

