"""Models and database functions"""

# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# db object - represents the database 
db = SQLAlchemy()

class User(db.Model):
    """User Login Information"""
   
    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    pw = db.Column(db.String(50), nullable=False)
    signup_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        """Prints user information"""
        return "<User user_id={} email={} signup_date={}".format(
            self.user_id, self.email, self.signup_date
        )


# Helper functions
def connect_to_db(app, db_uri="postgresql:///covid19"):
    """Connect database to Flask app"""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    # Run module interactively to work with database directly
    from server import app
    connect_to_db(app)
    print("Connected to database.")

# 1) createdb
# 2) python -i model.py
# 3) >>> db.create_all()
