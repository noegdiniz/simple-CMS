from flask_mail import Mail

mail = Mail()
def configure(app):
    app.config['MAIL_SERVER'] = 'smtp.example.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@example.com'
    app.config['MAIL_PASSWORD'] = 'your-email-password'
    app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'
    mail.init_app(app)