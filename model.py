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
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=False)
    state_name = db.Column(db.String(64), nullable=True)  # for testing purposes
    confirmed = db.Column(db.Integer, nullable=False)
    
    # Association relationship for city
    city_status = db.relationship("City", backref="status")


    def __repr__(self):
        """Provides info when printed"""
        return "<Status status_id={} status_date={} confirmed={}>".format(
            self.status_id, self.status_date, self.confirmed
        )
 


class City(db.Model):
    """Cities information"""

    __tablename__ = "cities"

    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String(64),  nullable=False)
    state_name = db.Column(db.String(64))


    def __repr__(self):
        """Provides info when printed"""
        return "<City city_id={} city_name={}>".format(
            self.city_id, self.city_name
        )



class Save(db.Model):
    """Cities saved by user."""

    __tablename__ = "saves"
    __table_args__ = (db.UniqueConstraint("user_id", "city_id"),)

    save_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    city_id = db.Column(db.Integer, db.ForeignKey("cities.city_id"))


    def __repr__(self):
        """Provide save info when printed."""
        return f"<Save save_id={self.save_id}, user_id={self.user_id}, city_id={self.city_id}>"



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
