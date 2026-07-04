from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40), unique = True, nullable = False)
    email = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    phone = db.Column(db.String(15), nullable = False)
    role = db.Column(db.String(20), nullable = False, default = "user") 
    status = db.Column(db.String(20), nullable = False, default = "active")

    managed_treks = db.relationship("Trek", back_populates = "staff", lazy = True)
    bookings = db.relationship("Booking", back_populates = "user", lazy = True)

    def __repr__(self):
        return f"<User {self.username}>"



class Trek(db.Model):
    __tablename__ = "treks"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    location = db.Column(db.String(100), nullable = False)
    difficulty = db.Column(db.String(20), nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    available_slots = db.Column(db.Integer, nullable = False)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id")) # for the trip guide
    status = db.Column(db.String(20), default = "Pending")
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))

    staff = db.relationship("User", back_populates = "managed_treks")

    bookings = db.relationship("Booking", back_populates = "trek", lazy = True)

    def __repr__(self):
        return f"<Trek {self.name}>"
    

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer,db.ForeignKey("treks.id"), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Booked")
    payment_status = db.Column(db.String(20))

    user = db.relationship("User", back_populates="bookings")

    trek = db.relationship("Trek", back_populates="bookings")

    def __repr__(self):
        return f"<Booking {self.id}>"