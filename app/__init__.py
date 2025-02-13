from flask import Flask
from app.ext import db, migrate
from app.blueprints import main
from app.admin import admin
from app.login import login, user_datastore
from app.mail import mail
from flask_babel import Babel

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    
    babel = Babel(app)

    db.configure(app)
    migrate.configure(app)
    main.configure(app)
    mail.configure(app)
    admin.configure(app)
    login.configure(app, user_datastore)
    user_datastore.configure(app)


    return app
