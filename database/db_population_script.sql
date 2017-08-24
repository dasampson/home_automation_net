/*

db_population_script.sql

This script can be used to populate the database created by the database 
creation script. 

*/

INSERT INTO lk_unit VALUES
(1, '°f', 'degrees Fahrenheit'),
(2, 'hPa', 'hectopascals'),
(3, '% RH', 'percent relative humidity');

INSERT INTO lk_event_level VALUES
(1, 'fat', 'Fatal'),
(2, 'err', 'Error'),
(3, 'wrn', 'Warn'),
(4, 'inf', 'Informational'),
(5, 'dbg', 'Debug');

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
(2, 'Garage Door Controller', 'This device controls the garage door and provides status on whether it is open or not. It also senses temperature, barometric pressure, and relative humidity.');

INSERT INTO nodes VALUES
(1, 'Office Environment Sensors', 1, 1, 'automation-office', '192.168.1.10'),

INSERT INTO events VALUES
(1, 'Garage Opened', 'Garage door has been opened.', 4),
(2, 'Garage Closed', 'Garage door has been closed.', 4),
(3, 'Garage Open Initiated', 'Garage door open has been initiated by controller.', 4),
(4, 'Garage Close Initiated', 'Garage door close has been initiated by controller.', 4),
(5, 'Garage Open Failed', 'Garage door is already open.', 2),
(6, 'Garage Close Failed', 'Garage door is already closed.', 2);