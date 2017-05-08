#!/usr/bin/python

from flask import Flask, request, Response
import json
from Adafruit_BMP085 import BMP085

app = Flask(__name__)

node_id = ''
bmp = BMP085(0x77)

def get_temp_f():
    bmp085_temp_c = bmp.readTemperature()
    bmp085_temp_f = (bmp085_temp_c * 9/5) + 32

    return bmp085_temp_f

def get_pressure():
    bmp085_pressure = bmp.readPressure()/100

    return bmp085_pressure

@app.route('/sensor_readings/', methods=['GET'])
def return_sensor_readings():
    temperature = get_temp_f()
    pressure = get_pressure()

    post_data = [ {"value":temperature, "unit_id":1}, {"value":pressure, "unit_id":2} ]
    data = json.dumps(post_data)
    resp = Response(data, status=200, mimetype='application/json')
    
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
