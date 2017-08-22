#!/usr/bin/python

from flask import Flask
from api_sensors import api_sensors
from api_garage import api_garage

app = Flask(__name__)


#app.register_blueprint(api_sensors)
#app.register_blueprint(api_garage)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

