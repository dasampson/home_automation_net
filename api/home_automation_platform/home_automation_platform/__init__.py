#!/usr/bin/python

from flask import Flask, request, Response
import psycopg2

app = Flask(__name__)

# Settings for Database calls
db_host = ''
db_port = '5432'
db_name = 'automation_data'
db_user = 'postgres'
db_pass = ''
timestamp = 'now()'

def run_db_query(query):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/sensor_records/<int:node_id>', methods=['POST'])
def log_sensor_record(node_id):
    content = request.get_json(force=True)

    run_db_query("INSERT INTO sensor_records VALUES (DEFAULT, {0:0.2f}, {1}, '{2}', '{3}');".format(content['temperature'], '1', timestamp, node_id))
    run_db_query("INSERT INTO sensor_records VALUES (DEFAULT, {0:0.2f}, {1}, '{2}', '{3}');".format(content['pressure'], '2', timestamp, node_id))
    run_db_query("INSERT INTO sensor_records VALUES (DEFAULT, {0:0.2f}, {1}, '{2}', '{3}');".format(content['humidity'], '3', timestamp, node_id))

    resp = Response('{ "status":"success" }', status=200, mimetype='application/json')
    return resp

@app.route('/event_records/<int:node_id>', methods=['POST'])
def log_event_record(node_id):
    content = request.get_json(force=True)

    run_db_query("INSERT INTO event_records VALUES (DEFAULT, {0}, '{1}', '{2}');".format(content['event_id'], timestamp, node_id))

    resp = Response('{ "status":"success" }', status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
