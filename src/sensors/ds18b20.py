#!/bin/python

import os
import glob
import time
from prettytable import PrettyTable
import jsonify
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def c2f(c):
    return (c * 9/5) + 32

class ds18b20():
    METRIC=False
    NAME="ds18b20"

    def __init__(self, METRIC=False):
        return None

    def getAliasForSensor(self, sensor_id):
        return sensor_id
        if sensor_id in os.environ:
            alias_id = "sensor_" + sensor_id.replace('28-','')
            return os.environ.get(alias_id)
        else:
            return sensor_id
    
    def get_sensor_ids(self):
        base_dir = '/sys/bus/w1/devices/'
        NUM_SENSORS = len(glob.glob(base_dir + '28*'))
        sensor_ids=[]
        for x in range(0,NUM_SENSORS):
            device_folder = glob.glob(base_dir + '28*')[x]
            id = device_folder.replace("/sys/bus/w1/devices/",'')
            sensor_ids.append(id)
        return sensor_ids

    #print get_sensor_ids()

    def read_temp_raw(self, sensor_id):
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + sensor_id)[0]
        device_file = device_folder + '/w1_slave'
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def read_temp(self, sensor_id):
        lines = self.read_temp_raw(sensor_id)
        return self.processData(lines)

    def processData(self, lines):
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
    #        return temp_c, temp_f
            return temp_f

    def display_temperature(self):
        sensor_tbl = PrettyTable(['Sensor','Value'])
        #sensor_vals = self.get_sensors()
        for sensor in self.get_sensor_ids():
            sensor_tbl.add_row([sensor, self.read_temp(sensor) ])
        print(sensor_tbl)

    def get_readings(self):
        SENSOR_IDS=self.get_sensor_ids()
        sensors_values = dict()
        for sensor in SENSOR_IDS:
            if sensor is not None:
                temp = self.read_temp(sensor)
                if not self.METRIC:
                    temp = c2f(temp)
                sensor_id = self.getAliasForSensor(sensor)
                sensors_values[sensor_id] = temp
                
        return sensors_values

    def get_reading(self, sensor):
        sensors_values = dict()
        if True:
            if sensor is not None:
                temp = self.read_temp(sensor)
                if not self.METRIC:
                    temp = c2f(temp)
                sensor_id = self.getAliasForSensor(sensor)
                sensors_values[sensor_id] = temp
        return sensors_values

    def get_sensors(self):
        d = dict()
        for s in self.get_sensor_ids():
            d[s] = self.read_temp(s)
        return d

    def get(self):
        return self.get_sensors()

    def get_dict(self):
        tld = dict()
        tld[self.NAME] = self.get()
        return tld
    
    def get_json(self):
        return jsonify(self.get_dict())

        

if __name__ == "__main__":
    sensor = ds18b20()
    while True:
        sensor.display_temperature()
        print(sensor.get_dict())
        time.sleep(1)
