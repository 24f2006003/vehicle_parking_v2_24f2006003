from flask import Flask
from application.config import Config, LocalDevelopmentConfig
from application.database import db
from application.models import User
from application.security import jwt

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    app.app_context().push()
    db.create_all()
    if not User.query.filter_by(role="admin").first():
        admin = User(username="admin", email="admin@example.com", password="admin", role="admin")
        db.session.add(admin)
        db.session.commit()
    return app

app = create_app()

from application.routes import *

if __name__ == "__main__":
    app.run()