from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False, default="user")

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A') # status: 'A' = available, 'O' = occupied

    lot = db.relationship('ParkingLot', backref=db.backref('spots', lazy=True))

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
    vehicle_number = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, nullable=False, default='active')  # active OR completed

    spot = db.relationship('ParkingSpot', backref=db.backref('reservations', lazy=True))
    user = db.relationship('User', backref=db.backref('reservations', lazy=True))


