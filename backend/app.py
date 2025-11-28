from flask import Flask
from application.config import Config, LocalDevelopmentConfig
from application.database import db
from application.models import User, ParkingLot, ParkingSpot
from application.security import jwt
from flask_cors import CORS
from application.celery_init import celery_init_app
from celery.schedules import crontab
from flask.json.provider import DefaultJSONProvider
from datetime import datetime, date

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    from application.cache import cache
    cache.init_app(app)
    CORS(app)
    app.app_context().push()
    db.create_all()
    
    # Seed admin
    if not User.query.filter_by(role="admin").first():
        admin = User(username="admin", email="admin@example.com", password="admin", role="admin")
        db.session.add(admin)
        db.session.commit()
        
    # Seed demo lots
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
            db.session.flush()
            for _ in range(lot["number_of_spots"]):
                db.session.add(ParkingSpot(lot_id=pl.id, status='A'))
        db.session.commit()

    class CustomJSONProvider(DefaultJSONProvider):
        def default(self, obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            return super().default(obj)

    app.json = CustomJSONProvider(app)

    return app

app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    from application.tasks import daily_reminder, monthly_report
    
    sender.add_periodic_task(
        120.0,
        daily_reminder.s(),
        name='daily-reminder'
    )
    
    sender.add_periodic_task(
        300.0,
        monthly_report.s(),
        name='monthly-report'
    )

from application.routes import *

if __name__ == "__main__":
    app.run()