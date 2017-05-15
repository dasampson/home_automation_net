#!/usr/bin/python

from flask import Flask, request, Response
import json
import BME280

app = Flask(__name__)

@app.route('/sensors/all', methods=['GET'])
def return_sensor_readings():
    temperature, pressure, humidity = BME280.readAllSensors()

    post_data = [ {"value":temperature, "unit_id":1}, {"value":pressure, "unit_id":2}, { "value":humidity, "unit_id":3 } ]
    data = json.dumps(post_data)
    resp = Response(data, status=200, mimetype='application/json')
    
    return resp

@app.route('/sensors/temperature', methods=['GET'])
def return_sensor_readings():
    temperature, pressure, humidity = BME280.readAllSensors()

    post_data = [ {"value":temperature, "unit_id":1} ]
    data = json.dumps(post_data)
    resp = Response(data, status=200, mimetype='application/json')
    
    return resp

@app.route('/sensors/pressure', methods=['GET'])
def return_sensor_readings():
    temperature, pressure, humidity = BME280.readAllSensors()

    post_data = [ {"value":pressure, "unit_id":2} ]
    data = json.dumps(post_data)
    resp = Response(data, status=200, mimetype='application/json')
    
    return resp

@app.route('/sensors/humidity', methods=['GET'])
def return_sensor_readings():
    temperature, pressure, humidity = BME280.readAllSensors()

    post_data = [ { "value":humidity, "unit_id":3 } ]
    data = json.dumps(post_data)
    resp = Response(data, status=200, mimetype='application/json')
    
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
