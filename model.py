"""Models and database functions"""

# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# db object - represents the database 
db = SQLAlchemy()

# USERS
class User(db.Model):
    """User Login Information"""
   
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    pw = db.Column(db.String(50), nullable=False)
    signup_date = db.Column(db.Date, nullable=False)

    # User relationships with saves & city
    saves = db.relationship("City", secondary="saves",
                                    backref="users")

    def __repr__(self):
        """Prints user information"""
        return "<User user_id={} email={} signup_date={}".format(
            self.user_id, self.email, self.signup_date
        )


# SAVES
class Save(db.Model):
    """Cities saved by user."""

    __tablename__ = "saves"
    __table_args__ = (db.UniqueConstraint("user_id", "city_id"),)

    save_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    city_id = db.Column(db.Integer, db.ForeignKey("cities.city_id"))


    def __repr__(self):
        """Provide save info when printed."""

        return f"<Save save_id={self.save_id}, user_id={self.user_id}, city_id={self.city_id}>"


    def add_saves(self, city):
        """Instantiates new saved city for user"""
        self.saves.append(city)


    def get_user_saves(self):
        """Get user's saved city_ids"""

        city_id_tups = db.session.query(Save.city_id).filter(Save.user_id == self.user_id).all()

        city_ids = []
        for tuple_ in city_id_tups:
            (city_id,) = tuple_
            city_ids.append(city_id)

        return city_ids


# STATES
class State(db.Model):
    """State information"""

    __tablename__ = "states"

    state_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_name = db.Column(db.String(50), nullable=False, unique=True)
    postal_code = db.Column(db.String(2), nullable=False, unique=True)


    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<State state_id={} state_name={}>".format(
            self.state_id, self.state_name
        )


# CITIES
class City(db.Model):
    """Cities information"""

    __tablename__ = "cities"

    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String(64), nullable=False, unique=True)
    # Foreign Key
    state_id = db.Column(db.Integer, db.ForeignKey("states.state_id"))
    
    # Backref to States
    states = db.relationship("State", backref="city")



    def __repr__(self):
        """Provides info when printed"""
        return "<City city_id={} city_name={}>".format(
            self.city_id, self.city_name
        )


class Status(db.Model):
    """Case information"""

    __tablename__ = "status"

    status_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    status_date = db.Column(db.Date, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Integer, nullable=False)

    # Status relationship with cities
    city = db.relationship("City", backref="status")


    def __repr__(self):
        """Provides info when printed"""
        return "<Status status_id={} status_date={} deaths={} confirmed={}>".format(
            self.status_id, self.status_date, self.deaths, self.confirmed
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

#dropdb db_name