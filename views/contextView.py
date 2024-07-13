from flask import request, jsonify
from flask import Blueprint
from flask_socketio import send, emit
from services import contextService
from utils import httpResponse
from config import context
from app import socketio
import time

contextBp = Blueprint('context', __name__, url_prefix='/context')

@contextBp.route('', methods=['POST', 'GET'])
def context():
    if request.method == 'POST':
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No input data provided"}), 400
        contextService.setContext(payload)
        return httpResponse.success({"message":"success"})
    elif request.method == 'GET':
        response = contextService.getContext()
        return httpResponse.success(response)
    
@socketio.on('connect')
def connect():
    print('client connected')
    
@socketio.on('get_params')
def handle_get_params(payload):
    while payload['connect']:
        socketio.emit('get_params', contextService.getContext())
        time.sleep(1)

