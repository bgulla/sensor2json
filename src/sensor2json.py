import logging
import sys
import requests
from flask import Flask, render_template, redirect, url_for, request, session, flash, g, abort, Blueprint, jsonify, session
from flask_restplus import Api, Resource, fields
import json
import os
import socket
from contextlib import closing
from werkzeug.contrib.fixers import ProxyFix
from sensors.sensehatsensor import SensehatSensor
import uuid


app = Flask(__name__)
app.secret_key = uuid.uuid4()

# Fix the swagger http proxy bug
app.wsgi_app = ProxyFix(app.wsgi_app)
api_v1 = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_v1, version='1.0', title='sensor2json',
    description='A Python3-based sensor tool for the Raspberry-Pi.',
)
ns = api.namespace('sensor2json', description='spitting out delicious sensor data.')

# ENV-based vars
FLASK_PORT = int(os.getenv('FLASK_PORT', 8080))
BLANK = ""

def abort_if_todo_doesnt_exist(todo_id):
    if False:
        api.abort(404, "Todo {} doesn't exist".format(todo_id))

@ns.route('/sensors')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.doc(description='Returns all the available sensor data')
    def get(self):
        '''Fetch a given resource'''
        #abort_if_todo_doesnt_exist(zipcode_id) # Replace this with syntax checker
        #return zipcodes.matching(str(zipcode_id))
        s = SensehatSensor()
        sensors = dict()
        sensors['sensehat'] = s.get()
        #return json.dumps(s.get(), ensure_ascii=True,indent=4,sort_keys=True)
        return jsonify(sensors)
        
@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stdout.
        app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        app.logger.setLevel(logging.INFO)

if __name__ == '__main__':
    app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    app.logger.setLevel(logging.INFO)
    # TODO: Copy logger from the other example
    app.register_blueprint(api_v1)
    app.config['SWAGGER_UI_DOC_EXPANSION'] = "full"

    # Fix the getuid bug
    os.environ["USER"] = "1001"
    app.run(port=5000, debug=True, host="0.0.0.0")