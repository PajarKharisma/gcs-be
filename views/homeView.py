import os

from flask import Blueprint
from utils import httpResponse

homeBp = Blueprint('home', __name__)

@homeBp.route('/', methods = ['GET'])
@homeBp.route('/home', methods = ['GET'])
def index():
    data = {
        "message" : f'Welcome to Krakatau GCS API version {os.environ.get("VERSION")}',
    }
    return httpResponse.success(data)