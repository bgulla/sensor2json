#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import logging
from prettytable import PrettyTable
from sense_hat import SenseHat
import jsonify

logger = logging.getLogger(__name__)

def c2f(c):
	return (c * 9/5) + 32

class SensehatSensor():
	METRIC = False
	sense = None
	NAME = "sensehat"

	def __init__(self, metric=False):
		"""
		Initializes the Slack client library.
		"""
		if metric:
			self.METRIC = True
		try:
			self.sense = SenseHat()
		except:
			return None
	
	def get_sensors(self):
		vals = dict()

		vals["humidity"] = self.sense.get_humidity() # Float	The percentage of relative humidity.
		vals["temperature"] = self.sense.get_temperature()
		vals["temperatureFromPressureSensor"] = self.sense.get_temperature_from_pressure()
		vals["pressure"] = self.sense.get_pressure() # Float	The current pressure in Millibars.

		# Make corrections for the non-metric folks out there
		if not self.METRIC:
			vals["temperature"] = c2f(vals["temperature"])
			vals["temperatureFromPressureSensor"] = c2f(vals["temperatureFromPressureSensor"])
		return vals
	
	def get(self):
		return self.get_sensors()
	
	def get_dict(self):
		s = dict()
		s[self.NAME] = self.get()
		return s
	
	def get_json(self):
		return jsonify( self.get_dict() )

def main():
	sensor = SensehatSensor()
	sensor_tbl = PrettyTable(['Sensor','Value'])
	sensor_vals = sensor.get_sensors()
	for key in sensor_vals.keys():
		sensor_tbl.add_row([key, sensor_vals[key] ])

	print(sensor_tbl)

if __name__ == "__main__":
	main()