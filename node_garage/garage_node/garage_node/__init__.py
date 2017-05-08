#!/usr/bin/python

from flask import Flask, request, Response
import json
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GARAGEPIN = 23
GPIO.setup(GARAGEPIN, GPIO.OUT)
GPIO.output(GARAGEPIN, GPIO.LOW)

@app.route('/door/close', methods=['PUT'])
def garage_close():
    GPIO.output(GARAGEPIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(GARAGEPIN, GPIO.LOW)

    resp = Response('{ "status":"success" }', status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
