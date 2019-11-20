from flask import Flask
from flask import Response
from flask import request
from flask_cors import CORS
from api_world import api_world
from src.db.dba import DBAccessor
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




















###################################################### TEST APIs ##########################################################

# @app.route('/home')
# def second_index():
#     return "brave new home!"

@app.route('/tablenames')
def server_status():
    dba = DBAccessor()
    obj = { "TableNames": dba.get_table_names() }
    return makeResponse(obj)

@app.route('/get/player/<string:id>')
def get_player(id):
    dba = DBAccessor()
    obj = { "player": dba.get_player(id) }
    return makeResponse(obj)

@app.route('/put/player/<string:id>')
def put_player(id):
    dba = DBAccessor()
    obj = { "player": dba.create_player({
        'id': {'S': id},
        'name': {'S':'player-name'},
        'court': {'S': 'court-id'},
        'status': {'S': 'status'}
    }) }
    return makeResponse(obj)

@app.route('/courts')
def get_courts():
    dba = DBAccessor()
    obj = { 'courts': dba.get_courts()}
    return makeResponse(obj)

# @app.route('/add/<string:table>', methods=['POST', 'OPTIONS'])
# def add_to_table(table):
#     if (request.method == 'OPTIONS'):
#         return makeOptionsResponse()
#     content = request.json
#     return makeResponse({'content': content})

if __name__ == '__main__':
    app.run(debug=True)