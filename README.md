# sensors2json
Exposes GPIO sensor data via JSON REST endpoint. This repo builds an ARM compatible Docker image that will output the values of DS18B20|BMP180 sensors connected to a Raspberry Pi.

## GPIO Sensors are hard, use REST!
The container binds to a provided port and outputs the sensor data in easy to ingest JSON blobs. 

```bash
🍺  pi@bar[~] > curl http://bar.local:8800/stats | jq "."
{
  "bmp180": {},
  "ds18b20": {
    "28-00000483ba1a": 67.4366,
    "28-00000471c98d": 39.5366
  }
}
```

## Requirements
###DS18B20 Temperature Sensor
[Adafruit has an awesome guide](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20) but in short do the following commands:

```bash
echo 'dtoverlay=w1-gpio' >> /boot/config.txt

echo 'w1-gpio' >> /etc/modules

echo 'w1-therm' >> /etc/modules

reboot
```
###BMP180 Temperature/Barometric/Altitude Sensor
`echo "dtparam=i2c1=on" >> /boot/config.txt`

`echo "dtparam=i2c_arm=on">> /boot/config.txt`

`echo "i2c-dev" >> /etc/modules`

`reboot`

## How to build
Building the image is straight forward:

* Git clone this repo
* `docker build -t hypriot-ds18b20`
* or `docker-compose up`

## Aliases
Sensor IDs don't tell a story, but aliases do. All DS18b20 sensors have an id in the format `28-<sensor_id>`. If you attach environment variables prepended with 'sensor_', the webserver will actually replace the sensor id with a string value.

Example:
`docker run -t -p 8080:8080 -v "/sys/bus/w1/devices:/sys/bus/w1/devices" -e 'sensor_00000483ba1a=chiller' containername`
