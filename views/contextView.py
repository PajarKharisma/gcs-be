from flask import request, jsonify
from flask import Blueprint
from services import contextService
from utils import httpResponse
from config import context

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