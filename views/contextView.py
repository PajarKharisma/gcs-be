from flask import request
from flask import Blueprint
from services import contextService
from utils import httpResponse
from config import context

contextBp = Blueprint('context', __name__, url_prefix='/context')

@contextBp.route('/set-input', methods=['POST'])
def setInput():
    payload = dict(request.json)
    contextService.setContext(payload, 'INPUT')
    return httpResponse.success({"message":"success"})

@contextBp.route('/set-output', methods=['POST'])
def setOutput():
    payload = dict(request.json)
    contextService.setContext(payload, 'OUTPUT')
    return httpResponse.success({"message":"success"})

@contextBp.route('/get-input', methods=['GET'])
def getInput():
    response = contextService.getContext('INPUT')
    return httpResponse.success(response)

@contextBp.route('/get-output', methods=['GET'])
def getOutput():
    response = contextService.getContext('OUTPUT')
    return httpResponse.success(response)