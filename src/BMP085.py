import Adafruit_BMP.BMP085 as BMP085sensor
import json
import os

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

class BMP085():

    is_active = True

    try:
        sensor = BMP085sensor.BMP085()
    except:
        print "[DISABLED] BMP Module"
        is_active = False

    def __int__(self):
        """

        :return:
        """
        return

    def get_temperature(self, format="F"):
        """

        :param format:
        :return:
        """
        if format == "F":
            return (self.sensor.read_temperature() * 9/5 +32)
        elif format == "C":
            return self.sensor.read_temperature()
        else:
            print "[BMP085] invalid format"

    def get_humidity(self):
        """

        :return:
        """
        return -1

    def get_altitude(self):
        """

        :return:
        """
        return self.sensor.read_altitude()

    def get_pressure(self):
        """

        :return:
        """
        return self.sensor.read_pressure()

    def get_JSON(self):
        """

        :return:
        """
        output = dict()
        sensor_name = 'BMP_085'
        output[sensor_name] = dict()
        try:
            output[sensor_name]['temperature'] = self.get_temperature("F")
            output[sensor_name]['temperatureC'] = self.get_temperature("C")
            output[sensor_name]['altitude'] = self.get_altitude()
            output[sensor_name]['pressure'] = self.get_pressure()
            output[sensor_name]['humidity'] = self.get_humidity()
        except:
            return json.dumps(output, ensure_ascii=False)
        return json.dumps(output, ensure_ascii=False)

    def get(self):
        """

        :return:
        """
        output = dict()
        sensor_name = 'bmp085'
        output[sensor_name] = dict()
        try:
            output[sensor_name]['temperature'] = self.get_temperature("F")
            output[sensor_name]['temperatureC'] = self.get_temperature("C")
            output[sensor_name]['altitude'] = self.get_altitude()
            output[sensor_name]['pressure'] = self.get_pressure()
            output[sensor_name]['humidity'] = self.get_humidity()
        except:
            return output
        return output


if __name__ == "__main__":
    sensor = BMP085()
    print "[BMP085]"
    print "[Temperature-F] ", sensor.get_temperature("F")
    print "[Temperature-C] ", sensor.get_temperature("C")
    print "[Altitude]", sensor.get_altitude()
    print "[Pressure]", sensor.get_pressure()
    print "[Humidity]", sensor.get_humidity()

