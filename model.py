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
    
    saves = db.relationship("County", secondary="saves",
                                    backref="users")

    def __repr__(self):
        """Prints user information"""
        return "<User user_id={} email={} signup_date={}".format(
            self.user_id, self.email, self.signup_date
        )


class County(db.Model):
    """County information"""

    __tablename__ = "counties"

    county_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    county_name = db.Column(db.String(64), nullable=False)
    state_name = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

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


class Confirmed(db.Model):
    """Confirmed number of people tested positive for COVID"""

    __tablename__ = "confirmed"

    confirmed_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.county_id'), nullable=False)
    state_name = db.Column(db.String(64), nullable=True) 
    confirmed = db.Column(db.Integer, nullable=False)
    
    # Association relationship for city
    county_confirmed = db.relationship("County", backref="confirmed")

    def __repr__(self):
        """Provides info when printed"""
        return "<Confirmed status_id={} status_date={} confirmed={}>".format(
            self.confirmed_id, self.date, self.confirmed
        )
 

class Fatality(db.Model):
    """Information on fatalities from COVID"""

    __tablename__ = "fatalities"

    fatality_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    county_id = db.Column(db.Integer, 
                          db.ForeignKey('counties.county_id'), nullable=False)
    state_name = db.Column(db.String(64), nullable=True) 
    fatalities = db.Column(db.Integer, nullable=False)

    # Association relationship for city
    county_fatality = db.relationship("County", backref="fatalities")

    def __repr__(self):
        """Provides info when printed"""
        return "<Fatality fatality_id={} fatality_date={} fatalities={}>".format(self.fatality_id, self.date, self.fatalities)


class USA(db.Model):
    """Information on USA total confirmed & fatality numbers"""

    __tablename__ = "usa"

    total_id = db.Collumn(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    confirmed_total = db.Column(db.Integer, nullable=False)
    fatality_total = db.Column(db.Integer, nullable=False)
    # recovered_total = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provides info when printed"""
        return f"<USA total_id={self.total_id} date={self.date} confirmed_total={self.confirmed_total} fatality_total={self.fatality_total}"



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
