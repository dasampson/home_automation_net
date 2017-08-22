#!/usr/bin/python

from flask import Flask, request, Response, Blueprint
import json
import BME280

api_sensors = Blueprint('api_sensors', __name__)

@api_sensors.route('/sensors/all', methods=['GET'])
def sensors_all():
    temperature, pressure, humidity = BME280.readAllSensors()

    post_data = [ {"value":temperature, "unit_id":1}, {"value":pressure, "unit_id":2}, { "value":humidity, "unit_id":3 } ]
    data = json.dumps(post_data)
    resp = Response(data, status=200, mimetype='application/json')
    
    return resp

@api_sensors.route('/sensors/temperature', methods=['GET'])
def sensor_temperature():
    temperature, pressure, humidity = BME280.readAllSensors()

    post_data = [ {"value":temperature, "unit_id":1} ]
    data = json.dumps(post_data)
    resp = Response(data, status=200, mimetype='application/json')
    
    return resp

@api_sensors.route('/sensors/pressure', methods=['GET'])
def sensor_pressure():
    temperature, pressure, humidity = BME280.readAllSensors()

    post_data = [ {"value":pressure, "unit_id":2} ]
    data = json.dumps(post_data)
    resp = Response(data, status=200, mimetype='application/json')
    
    return resp

@api_sensors.route('/sensors/humidity', methods=['GET'])
def sensor_humidity():
    temperature, pressure, humidity = BME280.readAllSensors()

    post_data = [ { "value":humidity, "unit_id":3 } ]
    data = json.dumps(post_data)
    resp = Response(data, status=200, mimetype='application/json')
    
    return resp

