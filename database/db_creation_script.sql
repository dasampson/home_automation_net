CREATE DATABASE automation_data;

\c automation_data

CREATE EXTENSION "uuid-ossp";

CREATE TABLE lk_unit
(
    unit_id SERIAL PRIMARY KEY,
    unit_shortname varchar(4) NOT NULL,
    unit_longname varchar(25)
);

CREATE TABLE lk_event_level
(
    event_level_id SERIAL PRIMARY KEY,
    level_shortname varchar(3) NOT NULL,
    level_longname varchar(15) NOT NULL
);

CREATE TABLE locations
(
	location_id SERIAL PRIMARY KEY,
	location_name varchar(15) NOT NULL
);

CREATE TABLE node_descriptions
(
	node_description_id SERIAL PRIMARY KEY,
	node_type varchar(25) NOT NULL,
	node_description varchar(150) NOT NULL
);

CREATE TABLE nodes
(
    node_id SERIAL PRIMARY KEY,
    name varchar(30) NOT NULL UNIQUE,
    node_description INTEGER,
    node_location INTEGER,
    FOREIGN KEY (node_location) REFERENCES locations (location_id),
    FOREIGN KEY (node_description) REFERENCES node_descriptions (node_description_id)
);

CREATE TABLE events
(
	event_id SERIAL PRIMARY KEY,
	event_shortname varchar(15) NOT NULL,
    event_description varchar(50) NOT NULL,
	level smallint NOT NULL,
	FOREIGN KEY (level) REFERENCES lk_event_level (event_level_id)
);

CREATE TABLE sensor_records
(
    sensor_record_uuid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    value numeric(10, 2) NOT NULL,
    unit_id smallint NOT NULL,
    sensor_record_timestamp timestamp WITH TIME ZONE NOT NULL DEFAULT current_timestamp,
    node_id INTEGER NOT NULL,
    FOREIGN KEY (unit_id) REFERENCES lk_unit (unit_id),
    FOREIGN KEY (node_id) REFERENCES nodes (node_id)
);

CREATE TABLE event_records
(
    event_record_uuid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id uuid NOT NULL,
    event_record_timestamp timestamp WITH TIME ZONE NOT NULL DEFAULT current_timestamp,
    node_id INTEGER NOT NULL,
    FOREIGN KEY (node_id) REFERENCES nodes (node_id)
);

INSERT INTO lk_unit VALUES
(1, '°f', 'degrees Fahrenheit'),
(2, 'hPa', 'hectopascals'),
(3, '% RH', 'percent relative humidity');

INSERT INTO lk_event_level VALUES
(1, 'fat', 'Fatal'),
(2, 'err', 'Error'),
(3, 'inf', 'Informational'),
(4, 'dbg', 'Debug');

INSERT INTO locations VALUES
(1, 'Office'),
(2, 'Back Yard'),
(3, 'Garage'),
(4, 'Bedroom'),
(5, 'Living Room'),
(6, 'Kitchen'),
(7, 'Dining Room');

INSERT INTO node_descriptions VALUES
(1, 'Environment Sensors', 'This type of sensor array detects ambient temperature, relative humidity, and barometric pressure.'),
(2, 'Garage Door Controller', 'This device controls the garage door and provides status on whether it is open or not.');

INSERT INTO nodes VALUES
(DEFAULT, 'Office Environment Sensors', 1, 1),
(DEFAULT, 'Back Yard Environment Sensors', 1, 2),
(DEFAULT, 'Garage Door Controller', 2, 3);

INSERT INTO events VALUES
(DEFAULT, 'Garage Opened', 'Garage door has been opened.', 3),
(DEFAULT, 'Garage Closed', 'Garage door has been closed.', 3);
