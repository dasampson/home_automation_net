#!/usr/bin/python

from flask import Flask, request, Response
import requests
import json
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

NODE_ID = '3'
HUB_HOST = 'automation-hub'

PIN_RELAY = 23
PIN_REEDSWITCH = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_REEDSWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_RELAY, GPIO.OUT)
GPIO.output(PIN_RELAY, GPIO.LOW)

def garage_activate():
    GPIO.output(PIN_RELAY, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(PIN_RELAY, GPIO.LOW)

def door_status_open():
    if GPIO.input(PIN_REEDSWITCH):
        return True
    else:
        return False

@app.route('/garage/open', methods=['PUT'])
def garage_open():
    if not door_status_open():
        garage_activate()
        resp = Response('{ "status":"success" }', status=200, mimetype='application/json')
        log_message = { "event_id":3 }
    else:
        resp = Response(status=304, mimetype='application/json')
        log_message = { "event_id":5 }

    log_post = requests.post("http://{0}/event_records/{1}".format(HUB_HOST, NODE_ID), json=log_message)
    return resp

@app.route('/garage/close', methods=['PUT'])
def garage_close():
    if door_status_open():
        garage_activate()
        resp = Response('{ "status":"success" }', status=200, mimetype='application/json')
        log_message = { "event_id":4 }
    else:
        resp = Response(status=304, mimetype='application/json')
        log_message = { "event_id":6 }

    log_post = requests.post("http://{0}/event_records/{1}".format(HUB_HOST, NODE_ID), json=log_message)
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
