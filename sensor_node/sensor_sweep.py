#!/usr/bin/python

import requests
import json
import Adafruit_DHT
from Adafruit_BMP085 import BMP085

platform_host = ''
node_id = ''

# DHT22 - Get Sensor Readings
sensor = Adafruit_DHT.DHT22
pin = 4
dht22_humidity, dht22_temp_c = Adafruit_DHT.read_retry(sensor, pin)
dht22_temp_f = (dht22_temp_c * 9/5) + 32

# BMP085 - Get Sensor Data
bmp = BMP085(0x77)
bmp085_temp_c = bmp.readTemperature()
bmp085_temp_f = (bmp085_temp_c * 9/5) + 32
bmp085_pressure = bmp.readPressure()/100

# Take average of temperatures for accuracy
combined_temp_c = (dht22_temp_c + bmp085_temp_c) / 2
combined_temp_f = (combined_temp_c * 9/5) + 32


post_data = [ {"value":combined_temp_f, "unit_id":1} ,{"value":bmp085_pressure, "unit_id":2}, { "value":dht22_humidity, "unit_id":3} ]

req = requests.post('http://'+platform_host+'/sensor_records/'+node_id, data=json.dumps(post_data))

req.status_code
