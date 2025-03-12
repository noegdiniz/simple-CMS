from datetime import datetime
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
    login.configure(app, user_datastore)
    user_datastore.configure(app)

    admin.configure(app)
    
    # Context processor to provide current year or datetime
    @app.context_processor
    def inject_current_time():
        return {
            'current_year': datetime.now().year,  # Just the year
            'current_datetime': datetime.now()     # Full datetime object if needed
        }

    # Optional: Custom datetime filter
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%Y'):
        if isinstance(value, datetime):
            return value.strftime(format)
        return value  # Fallback if not a datetime object
    
    return app
