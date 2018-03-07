#!/usr/bin/python
from flask import Flask, jsonify
from flask.ext.cors import CORS
import Adafruit_BMP.BMP085 as BMP085
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
sensor = BMP085.BMP085()


@app.route('/rest/api/v1.0/temperature', methods=['GET'])
def get_tasks():
    temp = sensor.read_temperature()
    temp = (temp * 9/5 +32)
    return str(temp)

@app.route('/stats', methods=['GET'])
def debug():
    sensors = dict()
    bmp180 = dict()
    bmp180['temperature'] = sensor.read_temperature()
    bmp180['temperatureF'] = (sensor.read_temperature() * 9/5 +32)
    bmp180['pressure'] = sensor.read_pressure()
    bmp180['altitude'] = sensor.read_altitude()
#    return json.dumps(bmp180, ensure_ascii=False)
    sensors['bmp180'] = bmp180
    return json.dumps(sensors, ensure_ascii=False)

@app.route('/temperature', methods=['GET'])
def get_tasks3():
    temp = sensor.read_temperature()
    temp = (temp * 9/5 +32)
    return str(temp)

@app.route('/rest/api/v1.0/pressure', methods=['GET'])
def get_val2():
    return str(sensor.read_pressure())

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8888)

