FROM resin/rpi-raspbian
MAINTAINER <blgulla@ncsu.edu>


RUN apt-get update; apt-get install -y git build-essential python-dev python-smbus apt-utils python-setuptools python-pip
RUN git clone https://github.com/adafruit/Adafruit_Python_BMP.git /data/adafruit ; cd /data/adafruit; python setup.py install
RUN git clone https://github.com/adafruit/Adafruit_Python_GPIO.git /data/adafruit_GPIO ; cd /data/adafruit_GPIO; python setup.py install
#RUN git clone https://github.com/adafruit/Adafruit_Python_BME280.git /data/adafruit_BME ; cd /data/adafruit_BME; python setup.py install

COPY ./requirements.txt /
RUN pip isntall -y /requirements.txt

COPY ./src /src
CMD ["python","/src/app.py"]
