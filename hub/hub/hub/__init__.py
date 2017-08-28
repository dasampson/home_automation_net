#!/usr/bin/python

from flask import Flask, request, Response
import requests
import psycopg2
import json

app = Flask(__name__)

# Settings for Database calls
db_host = 'automation-db'
db_port = '5432'
db_name = 'automation_data'
db_user = 'postgres'
db_pass = ''
timestamp = 'now()'

def db_insert(query):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def db_query(query):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return data

def get_node_id(ip_address)
    get_node_id = db_query("SELECT node_id FROM nodes WHERE node_ipaddress = '%s';" % ip_address)
    node_id = get_node_id[0][0]
    return node_id

@app.route('/', methods=['GET'])
def helo():
    resp = Response('Hello, World!', status=200, mimetype='text/plain')
    return resp

@app.route('/sensor_records', methods=['POST'])
def log_sensor_record():
    node_id = get_node_id(request.remote_addr)
    content = request.get_data()
    records = json.loads(content)

    for record in records:
        db_insert("INSERT INTO sensor_records VALUES (DEFAULT, {0:0.2f}, {1}, '{2}', '{3}');".format(record.get('value'), record.get('unit_id'), timestamp, node_id))
    
    resp = Response('{ "status":"success" }', status=200, mimetype='application/json')
    return resp

@app.route('/event_records', methods=['POST'])
def log_event_record():
    node_id = get_node_id(request.remote_addr)
    content = request.get_data()
    record = json.loads(content)

    db_insert("INSERT INTO event_records VALUES (DEFAULT, {0}, '{1}', '{2}');".format(record.get('event_id'), timestamp, node_id))

    resp = Response('{ "status":"success" }', status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
