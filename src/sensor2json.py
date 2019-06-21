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

app = Flask(__name__)
app.secret_key = '027f4073-a5ae-4ec6-a7e2-d7d0435a5867'

# Fix the swagger http proxy bug
app.wsgi_app = ProxyFix(app.wsgi_app)
api_v1 = Blueprint('api', __name__, url_prefix='/api/sensors')

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

@ns.route('/<string:zipcode_id>')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.doc(description='US Zip-codes only in Integer format')
    def get(self, zipcode_id):
        '''Fetch a given resource'''
        abort_if_todo_doesnt_exist(zipcode_id) # Replace this with syntax checker
        return zipcodes.matching(str(zipcode_id))


@app.route('/status', methods=['GET', 'POST']) #this is the meat
def healthcheck():
    return "HEALTHY"

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

    if True:
        app.run(port=FLASK_PORT, debug=True, host="0.0.0.0")
    else:
        app.run(port=8443, ssl_context=(CERT_FILE, KEY_FILE), debug=True, host="0.0.0.0")
