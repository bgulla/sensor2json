[![Build Status](https://travis-ci.org/bgulla/sensor2json.svg?branch=master)](https://travis-ci.org/bgulla/sensor2json)

# sensor2json
Exposes GPIO sensor data via JSON REST endpoint. This repo builds an ARM compatible Docker image that will output the values of [DS18B20](https://www.adafruit.com/product/381) or [BMP180](https://www.adafruit.com/product/2652) temperature/altitude/barometric pressure sensors connected to a Raspberry Pi. This library can be extended to serve up any GPIO sensors. Pull Requests are welcome. Built using Python Flask.

## GPIO Sensors are hard, use REST!
The container binds to a provided port and outputs the sensor data in easy to ingest JSON blobs. 

```bash
🍺  pi@bar[~] > docker run --rm -d --privileged -p 8800:8800 -t bgulla/sensor2json
🍺  pi@bar[~] > curl http://bar.local:8800/stats | jq "."
{
  "bmp180": { 
    "temperatureF": 69.25999999999999,
    "pressure": 100665,
    "altitude": 54.34029119011573,
    "temperature": 20.7
  },
  "ds18b20": {
    "28-00000483ba1a": 67.4366,
    "28-00000471c98d": 39.5366
  }
}
```

## Requirements
### DS18B20 Temperature Sensor
[Adafruit has an awesome guide](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20) but in short do the following commands:

```bash
echo 'dtoverlay=w1-gpio' >> /boot/config.txt
echo 'w1-gpio' >> /etc/modules
echo 'w1-therm' >> /etc/modules
reboot
```
### BMP180 Temperature/Barometric/Altitude Sensor
```bash
echo "dtparam=i2c1=on" >> /boot/config.txt
echo "dtparam=i2c_arm=on">> /boot/config.txt
echo "i2c-dev" >> /etc/modules
reboot
```

## How to build
Building the image is straight forward:

* Git clone this repo
* `docker build -t sensor2json`

## Aliases
Sensor IDs don't tell a story, but aliases do. All DS18b20 sensors have an id in the format `28-<sensor_id>`. If you attach environment variables prepended with 'sensor_', the webserver will actually replace the sensor id with a string value.

Example:
```bash
pi@bar[~] > docker run -t -p 8800:8800 -e 'sensor_00000483ba1a=kegerator' --privileged bgulla/sensor2json
pi@bar[~] > curl http://bar.local:8800/stats | jq "."
{
  "bmp180": {},
  "ds18b20": {
    "28-00000483ba1a": 67.4366,
    "kegerator": 39.5366
  }
}

```

## Telegraf/InfluxDB (+Grafana) Plugin
![Grafana is awesome](https://github.com/bgulla/sensor2json/raw/master/img/grafana.png?raw=true)
Graphs are awesome! I am am a huge fan of InfluxDB + Grafana. My shipping agent of choice is [Telegraf](https://github.com/influxdata/telegraf). Telegraf will parse the GET request to your rest endpoint and automagically send it to InfluxDB. 

Add the folllowing to your /etc/telegraf/telegraf.conf file:

```bash
[[inputs.httpjson]]
  name = "bar_stats"
# URL of each server in the service's cluster
  servers = [
    "http://localhost:8800/stats",
  ]
# Set response_timeout (default 5 seconds)
  response_timeout = "5s"
# HTTP method to use: GET or POST (case-sensitive)
  method = "GET"
```
