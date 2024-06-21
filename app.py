from flask import Flask
from flask_cors import CORS
import os
import atexit
import signal
import logging
from config import context
from jobs.serialJob import SerialThread

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

from views import *

logging.basicConfig(level=logging.INFO)

# Global variable to track the thread instance
serial_thread = None

def start_serial_thread():
    global serial_thread
    if serial_thread is None or not serial_thread.is_alive():
        logging.info("Starting serial thread...")
        serial_thread = SerialThread('serial_thread')
        serial_thread.daemon = True
        serial_thread.start()
    else:
        logging.info("Serial thread already running.")

start_serial_thread()

def cleanup():
    logging.info("Stopping background thread...")
    if serial_thread is not None:
        serial_thread.stop()
        serial_thread.join()

atexit.register(cleanup)

def handle_signal(signal, frame):
    cleanup()
    os._exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    context.VALUES['app_connect'] = False
