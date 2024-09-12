from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import atexit
import signal
import logging
from config import context
from jobs.serialJob import SerialThread
from jobs.antenaJob import AntenaThread

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
app.secret_key = os.urandom(24)

from views import *

logging.basicConfig(level=logging.INFO)

# Global variable to track the thread instance
serial_thread = None
antena_thread = None

def start_serial_thread():
    global serial_thread
    if serial_thread is None or not serial_thread.is_alive():
        logging.info("Starting serial thread...")
        serial_thread = SerialThread('serial_thread')
        serial_thread.daemon = True
        serial_thread.start()
    else:
        logging.info("Serial thread already running.")
    
def start_antena_thread():
    global antena_thread
    if antena_thread is None or not antena_thread.is_alive():
        logging.info("Starting antena thread...")
        antena_thread = AntenaThread('antena_thread')
        antena_thread.daemon = True
        antena_thread.start()
    else:
        logging.info("Antena thread already running.")

start_serial_thread()
start_antena_thread()

def cleanup():
    logging.info("Stopping background thread...")
    if serial_thread is not None:
        serial_thread.stop()
        serial_thread.join()
    if antena_thread is not None:
        antena_thread.stop()
        antena_thread.join()

atexit.register(cleanup)

def handle_signal(signal, frame):
    cleanup()
    os._exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=True)
    context.VALUES['app_connect'] = False
