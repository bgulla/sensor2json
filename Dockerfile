#FROM resin/raspberry-pi-python:2-wheezy
FROM resin/rpi-raspbian
MAINTAINER <blgulla@ncsu.edu>


RUN apt-get update; apt-get install -y git build-essential python-dev python-smbus apt-utils python-setuptools 
RUN apt-get install -y python-pip; 
RUN git clone https://github.com/adafruit/Adafruit_Python_BMP.git /data/adafruit ; cd /data/adafruit; python setup.py install
RUN pip install Flask flask-cors

COPY ./src /src
CMD ["python","/src/app.py"]
#CMD ["python","/data/adafruit/examples/simpletest.py"]
