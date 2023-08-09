from flask import Flask
from flask_cors import CORS
import os
import sys
from config import context

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

from views import *
from jobs.serialJob import SerialThread

if __name__ == "__main__":
    thrd = SerialThread('serial_thread')
    thrd.daemon = True
    thrd.start()

    app.run(host='0.0.0.0', port=5000)
    context.INPUT_VALUES['app_connect'] = False
    thrd.join()