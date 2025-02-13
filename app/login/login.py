from flask_security import Security

security = Security()

def configure(app, user_datastore):
    security.init_app(app, user_datastore.user_datastore)
    