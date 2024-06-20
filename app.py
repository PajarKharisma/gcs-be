from flask import Flask
from flask_cors import CORS
import os
import atexit
import signal
from config import context

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

from views import *
from jobs.serialJob import SerialThread

# Initialize the background thread
thrd = SerialThread('serial_thread')
thrd.daemon = True
thrd.start()

# Ensure the background thread stops when the application exits
def cleanup():
    print("Stopping background thread...")
    thrd.stop()
    thrd.join()

atexit.register(cleanup)

# Handle signals to ensure graceful shutdown
def handle_signal(signal, frame):
    cleanup()
    os._exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    context.VALUES['app_connect'] = False
