from flask import Flask
from application.config import Config, LocalDevelopmentConfig
from application.database import db
from application.models import User, ParkingLot, ParkingSpot
from application.security import jwt
from flask_cors import CORS

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    app.app_context().push()
    db.create_all()
    if not User.query.filter_by(role="admin").first():
        admin = User(username="admin", email="admin@example.com", password="admin", role="admin")
        db.session.add(admin)
        db.session.commit()
    # Seed demo parking lots and spots if none exist
    if ParkingLot.query.count() == 0:
        demo_lots = [
            {"prime_location_name": "Central Plaza", "price": 25.0, "address": "Main Road", "pin_code": 600001, "number_of_spots": 10},
            {"prime_location_name": "Beachfront Lot", "price": 35.0, "address": "Ocean Drive", "pin_code": 600104, "number_of_spots": 8},
            {"prime_location_name": "Airport South", "price": 45.0, "address": "Gateway Road", "pin_code": 600044, "number_of_spots": 12},
        ]
        for lot in demo_lots:
            pl = ParkingLot(
                prime_location_name=lot["prime_location_name"],
                price=lot["price"],
                address=lot["address"],
                pin_code=lot["pin_code"],
                number_of_spots=lot["number_of_spots"],
                available_spots=lot["number_of_spots"],
            )
            db.session.add(pl)
            db.session.flush()  # get pl.id
            # create spots
            for _ in range(lot["number_of_spots"]):
                db.session.add(ParkingSpot(lot_id=pl.id, status='A'))
        db.session.commit()
    return app

app = create_app()

from application.routes import *

if __name__ == "__main__":
    app.run()