#!/usr/bin/python
from flask import Flask, jsonify
from flask.ext.cors import CORS
import ds18b20
import BMP085
import bme280

import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

use_bmp = True

try:
    sensor = BMP085.BMP085()
except:
    print "[DISABLED] BMP Module"
    use_bmp = False


@app.route('/rest/api/v1.0/temperature', methods=['GET'])
def get_tasks():
    temp = sensor.read_temperature()
    temp = (temp * 9/5 +32)
    return str(temp)

# ds18b20
@app.route('/ds', methods=['GET'])
def get_tasks2():
    sensors = dict()
    sensors['ds18b20'] = ds18b20.get_readings()
    return json.dumps(sensors, ensure_ascii=False)

@app.route('/stats', methods=['GET'])
def debug():
    sensors = dict()
    # ds18b20 sensor
    sensors = dict()
    if ds18b20.get_sensor_ids() > 0:
        sensors['ds18b20'] = ds18b20.get_readings()
    #bmp sensor
    bmp180 = dict()
    if use_bmp:
        bmp180['temperature'] = sensor.read_temperature()
        bmp180['temperatureF'] = (sensor.read_temperature() * 9/5 +32)
        bmp180['pressure'] = sensor.read_pressure()
        bmp180['altitude'] = sensor.read_altitude()
    sensors['bmp180'] = bmp180
    sensors['bme280'] = bme280.BME280.get_JSON()
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
    app.run(host='0.0.0.0', port=8800)

