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
    return app

app = create_app()

from application.routes import *

if __name__ == "__main__":
    # db.create_all()
    # db.session.add(User(username="admin", email="admin@example.com", password="admin", role="admin"))
    # db.session.add(User(username="user", email="user@example.com", password="user"))
    # db.session.commit()

    app.run()