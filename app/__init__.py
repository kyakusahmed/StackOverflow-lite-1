from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config

app = Flask(__name__)

app.config.from_object('config.Config')
app.config['JWT_SECRET_KEY'] = 'wuiq2739%W%$%^FhjY^^'
jwt = JWTManager(app)
