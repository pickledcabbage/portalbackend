from flask import Flask
from flask import Response
from flask import request
from flask_cors import CORS
from api_world import api_world
from src.error.ServiceError import ServiceError
from src.activity.apis import *
import json

app = Flask(__name__)
CORS(app)

def makeResponse(obj):
    # Allows for JS requests from react app
    resp = Response(json.dumps(obj))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

def makeOptionsResponse():
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def makeBadResponse(message=''):
    resp = Response(json.dumps({"message":message}))
    resp.status_code = 400
    return resp


@app.route('/world', methods=['GET','POST', 'OPTIONS'])
def index():
    #Check if HTTP JSON is valid format
    #Maybe convert to python object

    #Do something here VVV
    if (request.method == 'OPTIONS'):
        return makeOptionsResponse()
    obj = api_world("something")
    return makeResponse(obj)

@app.route('/addplayer', methods=['POST'])
def add_player():
    if (request.method == 'OPTIONS'):
        return makeOptionsResponse()
    try:
        obj = api_add_player(request.json)
    except ServiceError:
        return makeBadResponse()
    return makeResponse(obj)

@app.route('/addtoqueue', methods=['POST'])
def add_to_queue():
    if (request.method == 'OPTIONS'):
        return makeOptionsResponse()
    try:
        obj = api_signup_group(request.json)
    except ServiceError as e:
        return makeBadResponse("<ServiceError>: "+e.message)
    except QueueError as e:
        return makeBadResponse(message=e.message)
    return makeResponse(obj)

@app.route('/getcourtdata')
def get_court_data():
    if (request.method == 'OPTIONS'):
        return makeOptionsResponse()
    obj = api_get_court_data()
    return makeResponse(obj)

@app.route('/drop', methods=['POST'])
def drop():
    if (request.method == 'OPTIONS'):
        return makeOptionsResponse()
    try:
        obj = api_drop_player(request.json)
    except ServiceError as e:
        return makeBadResponse(message=e.message)
    return makeResponse(obj)

@app.route('/playerstatus', methods=['POST'])
def get_status():
    if (request.method == 'OPTIONS'):
        return makeOptionsResponse()
    try:
        obj = api_get_player_status(request.json)
    except ServiceError as e:
        return makeBadResponse(message=e.message)
    return makeResponse(obj)


if __name__ == '__main__':
    app.run(debug=True)