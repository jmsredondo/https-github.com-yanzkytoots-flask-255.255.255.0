from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import TestingConfig

app = Flask(__name__)
app.config.from_object(TestingConfig)
db = SQLAlchemy(app)

from tests import app_tests, models
