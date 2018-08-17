from flask import Blueprint

mod = Blueprint('api', __name__)

from api import books, genres
