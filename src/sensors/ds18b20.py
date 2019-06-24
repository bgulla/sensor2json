#!/bin/python

import os
import glob
import time
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def c2f(c):
	return (c * 9/5) + 32

class ds18b20sensor():
	METRIC = False
	sense = None
	NAME = "sensehat"

    def __init__(self, metric=False):
        return

    def ctof(self, temp):
        return str(temp * 9.0 / 5.0 + 32.0)

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
    #    lines = read_temp_raw(get_sensor_ids()[0])
        lines = read_temp_raw(sensor_id)
        return processData(lines)

    def processData(self, lines):
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
    #        return temp_c, temp_f
            return temp_f

    def display_temperature(self):
        for sensor in get_sensor_ids():
            temp = self.read_temp(sensor)
            print "[ID] %s\t%s]" % (sensor,temp)
        
    
    def get_readings(self):
        SENSOR_IDS=get_sensor_ids()
        sensors_values = dict()
        for sensor in SENSOR_IDS:
            if sensor is not None:
                temp = read_temp(sensor)
                sensor_id = getAliasForSensor(sensor)
                sensors_values[sensor_id] = temp
        return sensors_values

    def get_reading(self, sensor):
        sensors_values = dict()
        if True:
            if sensor is not None:
                temp = read_temp(sensor)
                sensor_id = getAliasForSensor(sensor)
                sensors_values[sensor_id] = temp
        return sensors_values
        

if __name__ == "__main__":
    sensor = ds18b20sensor()
    while True:
   	    readings = sensor.get_reading('28-00000471c98d')
	    if readings is not None:
    	        for key in readings:
    	            if key is not None:
     	                print "[%s] %s" % (key, readings[key])
	    time.sleep(1)
