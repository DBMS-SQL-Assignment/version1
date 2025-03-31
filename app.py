from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db, User
<<<<<<< HEAD
from flask_jwt_extended import JWTManager
=======
>>>>>>> e542fb22b4fc97aa95d94e125a5ce237175610ea

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

<<<<<<< HEAD
jwt = JWTManager(app)

=======
>>>>>>> e542fb22b4fc97aa95d94e125a5ce237175610ea
# Flask-Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/api/login"



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
