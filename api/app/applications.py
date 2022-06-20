import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("REMINDER_SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("REMINDER_URL_DATABASE")
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("REMINDER_EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("REMINDER_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
database = SQLAlchemy(app)
serializer = Marshmallow(app)
urlSafe = URLSafeTimedSerializer(os.getenv("REMINDER_SECRET_KEY"))