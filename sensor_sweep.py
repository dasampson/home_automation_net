#!/usr/bin/python

import psycopg2
import Adafruit_DHT
from Adafruit_BMP085 import BMP085

# Settings for Database calls
node_name = 'Living Room'
timestamp = 'now()'


# DHT22 - Get Sensor Readings
sensor = Adafruit_DHT.DHT22
pin = 23
dht22_humidity, dht22_temp_c = Adafruit_DHT.read_retry(sensor, pin)
dht22_temp_f = (dht22_temp_c * 9/5) + 32

# BMP085 - Get Sensor Data
bmp = BMP085(0x77)
bmp085_temp_c = bmp.readTemperature()
bmp085_temp_f = (bmp085_temp_c * 9/5) + 32
bmp085_pressure = bmp.readPressure()

# Take average of temperatures for accuracy
combined_temp_c = (dht22_temp_c + bmp085_temp_c) / 2
combined_temp_f = (combined_temp_c * 9/5) + 32


# Open db connection
conn = psycopg2.connect(database='DATABASE_NAME_HERE', user='DB_USER_USERNAME_HERE', password='DB_USER_PASSWORD_HERE', host='IP_OR_HOSTNAME_FOR_SERVER', port='5432')
cursor = conn.cursor()


# Get sensor node ID
cursor.execute("SELECT sensor_node_id FROM sensor_nodes where name = '{0}' limit 1;".format(node_name))
node_id = cursor.fetchone()[0]


# Write sensor readings to database
cursor.execute("INSERT INTO sensor_readings VALUES (DEFAULT, {0:0.2f}, {1}, '{2}', '{3}');".format(combined_temp_f, '1', timestamp, node_id))
cursor.execute("INSERT INTO sensor_readings VALUES (DEFAULT, {0:0.2f}, {1}, '{2}', '{3}');".format((bmp085_pressure/100), '2', timestamp, node_id))
cursor.execute("INSERT INTO sensor_readings VALUES (DEFAULT, {0:0.2f}, {1}, '{2}', '{3}');".format(dht22_humidity, '3', timestamp, node_id))


# Commit transactions and close db connection
conn.commit()
cursor.close()
conn.close()

