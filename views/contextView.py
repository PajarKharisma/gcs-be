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
def context_index():
    if request.method == 'POST':
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No input data provided"}), 400
        contextService.setContext(payload)
        return httpResponse.success({"message":"success"})
    elif request.method == 'GET':
        response = contextService.getContext()
        return httpResponse.success(response)
    
@contextBp.route('/set-antena-pos', methods=['GET'])
def set_antena_pos():
    context.VALUES['antena_lat'] = context.VALUES['lat']
    context.VALUES['antena_long'] = context.VALUES['long']
    return httpResponse.success({"message":"success"})

@contextBp.route('/reset-antena-pos', methods=['GET'])
def reset_antena_pos():
    context.VALUES['antena_lat'] = 0
    context.VALUES['antena_long'] = 0
    return httpResponse.success({"message":"success"})
    
@socketio.on('connect')
def connect():
    print('client connected')
    
@socketio.on('get_params')
def handle_get_params(payload):
    while payload['connect']:
        socketio.emit('get_params', contextService.getContext())
        time.sleep(1)

