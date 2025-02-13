from flask_security import SQLAlchemyUserDatastore
from app.ext.db import db
from app.models.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def configure(app):
    pass
    