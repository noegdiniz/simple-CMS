import os
import string
import random


BASE_DIR = os.path.abspath('.')

SECRET_KEY = ''.join(random.choice(string.ascii_letters) for i in range(42))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')

# SQLALCHEMY_ECHO = True
BABEL_DEFAULT_LOCALE = 'pt_BR'
BABEL_TRANSLATION_DIRECTORIES = '/mnt/c/PROJETOS/github/simple-CMS/app/translations'

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True

SECURITY_SEND_PASSWORD_RESET_EMAIL = True

SECURITY_SEND_REGISTER_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECURITY_SEND_PASSWORD_RESET_EMAIL = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
