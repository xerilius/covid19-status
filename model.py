"""Models and database functions"""

# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    """User Login Information"""
   
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    signup_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    pw = db.Column(db.String(50), nullable=False)
    

    # saves = db.relationship("City", secondary="saves",
    #                                 backref="users")

    def __repr__(self):
        """Prints user information"""
        return "<User user_id={} email={} signup_date={}".format(
            self.user_id, self.email, self.signup_date
        )



class Status(db.Model):
    """Case information"""

    __tablename__ = "status"

    status_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    status_date = db.Column(db.Date, nullable=False)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.county_id'), nullable=False)
    state_name = db.Column(db.String(64), nullable=True)  # for testing purposes
    confirmed = db.Column(db.Integer, nullable=False)
    
    # Association relationship for city
    county_status = db.relationship("County", backref="status")


    def __repr__(self):
        """Provides info when printed"""
        return "<Status status_id={} status_date={} confirmed={}>".format(
            self.status_id, self.status_date, self.confirmed
        )
 


class County(db.Model):
    """County information"""

    __tablename__ = "counties"

    county_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    county_name = db.Column(db.String(64),  nullable=False)
    state_name = db.Column(db.String(64))
    # zipcode = db.Column(db.Integer, nullable=False)
    # latitude = db.Column(db.Integer)
    # longitude = db.Column(db.Integer)


    def __repr__(self):
        """Provides info when printed"""
        return "<County county_id={} county_name={}>".format(
            self.county_id, self.county_name
        )



class Save(db.Model):
    """Counties saved by user."""

    __tablename__ = "saves"
    __table_args__ = (db.UniqueConstraint("user_id", "county_id"),)

    save_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    county_id = db.Column(db.Integer, db.ForeignKey("counties.county_id"))


    def __repr__(self):
        """Provide save info when printed."""
        return f"<Save save_id={self.save_id}, user_id={self.user_id}, county_id={self.county_id}>"



# Helper functions
def connect_to_db(app, db_uri="postgresql:///covid19"):
    """Connect database to Flask app"""

    # Postgres DB Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    print("Connected to database.")
