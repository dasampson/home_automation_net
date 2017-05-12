#!/usr/bin/python

from flask import Flask, request, Response
import json
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

GARAGEPIN = 23
DOORPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DOORPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GARAGEPIN, GPIO.OUT)
GPIO.output(GARAGEPIN, GPIO.LOW)

def garage_activate():
    GPIO.output(GARAGEPIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(GARAGEPIN, GPIO.LOW)

def door_status_open():
	if not GPIO.input(DOORPIN):
		return True
	else:
		return False

@app.route('/garage/open', methods=['PUT'])
def garage_open():
    if door_status_open():
    	garage_activate()
    	resp = Response('{ "status":"success" }', status=200, mimetype='application/json')
    else:
    	resp = Response(status=304, mimetype='application/json')
    
    return resp

@app.route('/garage/close', methods=['PUT'])
def garage_close():
    if not door_status_open():
    	garage_activate()
    	resp = Response('{ "status":"success" }', status=200, mimetype='application/json')
    else:
    	resp = Response(status=304, mimetype='application/json')

    return resp

@app.route('/garage/status', methods=['GET'])
def garage_status():
    if door_status_open():
    	resp = Response('{ "status":"open" }', status=200, mimetype='application/json')
    else:
    	resp = Response('{ "status":"closed" }', status=200, mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
