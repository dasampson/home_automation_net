# Raspberry Pi Sensor Project
---
Driver code for the BMP085 and DHT22 sensors originated from Adafruit and has not been modified. For more information on setting up these sensors, please visit the Adafruit website. When properly implemented, this project enables you to use a Raspberry Pi to record and log the humidity, barometric pressure, and temperature. The database can be installed on one Raspberry Pi and then as many sensor nodes as desired can be added.

## Set Up the Raspberry Pi
---

### Required Hardware
- Raspberry Pi (1st or 2nd Gen Model B/B+)
- Optional: EdiMax WiFi Module
- 2.1 amp power supply
- MicroUSB Cable
- SD or MicroSD Card (Dependent on Model of Raspberry Pi)
- DHT22 Humidity and Temperature Sensor
- BMP085 Barometric Pressure and Temperature Sensor
- Breadboard
- Breadboard Jumper Wires (Male-to-Male)
- Breadboard Jumper Wires (Female-to-Male)
- 4.7k Ohm Resistor for DHT22 Sensor

### Install Required Packages
```
sudo apt-get install python-pip python-dev python-setuptools python-smbus libpq-dev postgresql postgresql-contrib
```

### Set the Timezone
1. Run the command: `sudo dpkg-reconfigure tzdata`
2. Select "US" or whatever country you wish.
3. Select "Pacific Ocean" for PST or something else for whichever timezone you need.

### Set Up WiFi (Optional)

### Add WiFi Credentials to the Supplicant File
1. Edit /etc/wpa_supplicant/wpa_supplicant.conf and add lines:
```
network={
	ssid="network name here"
	psk="network password here"
}
```

### Disable WiFi Module Power Management
1. Make the file /etc/modprobe.d/8192cu.conf
2. Add this line to the file:
`options 8192cu rtw_power_mgnt=0`
3. Reboot the Raspberry Pi.

# Set Up PostgreSQL
---

### Prepare PostgreSQL
1. Log into Postgres:
`sudo -u postgres psql`
2. Set a password for the postgres user:
`ALTER USER postgres WITH PASSWORD 'your password here';`
3. Add the uuid-ossp module to generate UUIDs for several fields:
`CREATE EXTENSION "uuid-ossp";`

### Allow Remote Database Access from Any Host
1. Edit the file /etc/postgresql/9.4/main/pg_hba.conf and add the line:
   ```
   host    all     all     0.0.0.0/0       md5
   ```
   
2. Edit the file /etc/postgresql/9.4/main/postgresql.conf and uncomment or add this line:
   ```
   listen_addresses = '*'
   ```

### Create the Database and Schema
1. Create the database:
   ```sql
   CREATE DATABASE sensor_data;
   ```
   
2. Create the tables: 
   ```sql
   CREATE TABLE lk_unit
   (
	   unit_id smallint PRIMARY KEY,
	   unit_shortname varchar(6) NOT NULL,
	   unit_longname varchar(25)
   );

   CREATE TABLE sensor_nodes
   (
	   sensor_node_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	   name varchar(25) UNIQUE
   );

   CREATE TABLE sensor_readings
   (
	   reading_uuid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	   reading_value numeric(10, 2) NOT NULL,
	   reading_unit_id smallint NOT NULL,
	   reading_timestamp timestamp WITH TIME ZONE NOT NULL DEFAULT current_timestamp,
	   sensor_node_id uuid NOT NULL,
	   FOREIGN KEY (reading_unit_id) REFERENCES lk_unit (unit_id),
	   FOREIGN KEY (sensor_node_id) REFERENCES sensor_nodes (sensor_node_id)
   );
   ```

### Insert Initial Data
1. The first record necessary to begin logging is at least one sensor node. Add one with this insert statement:
   
   ```sql
   INSERT INTO sensor_nodes VALUES (DEFAULT, 'Living Room');
   ```
   
2. The next records go into the lookup table for sensor reading units. Add the necessary records with these statements:
   
   ```sql
   INSERT INTO lk_unit VALUES 
   (1, 'f', 'degrees Fahrenheit'),
   (2, 'hPa', 'hectopascals'),
   (3, '% RH', 'percent relative humidity');
   ```

## Set Up the Sensors
---

### Set Up I2C
1. Edit /ect/modules and add lines:
   ```
   snd-bcm2835
   i2c-bcm2708
   i2c-dev
   ```
   
2. Edit /boot/config.txt and add lines:
   ```
   dtparam=i2c1=on
   dtparam=i2c_arm=on
   ```
   
3. Reboot the Raspberry Pi.
4. Connect the BMP085 sensor to the GPIO ports and run the command:
`sudo i2cdetect -y 1`
5. If this command doesn't work try a 0 instead of a 1. 
6. The command prints out connected devices. This example shows one BMP085 connected:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- 77    
```

### Setup the DHT22 Driver
1. Navigate to the folder with the DHT22 driver code:
`cd Adafruit_Python_DHT/`
2. Run the script to install the driver:
`sudo python setup.py install`
3. Navigate to the examples folder inside the Adafruit_Python_DHT folder:
`cd examples/`
4. Edit the `simpletest.py` file and ensure the sensor and pin are set correctly.
5. Run the `simpletest.py` file and ensure that sensor readings are returned.

### Set Up a Cronjob to Run the Script Gathering Sensor Readings
1. Use this command to edit the cronjob file:
`sudo crontab -e`
2. Add this line to execute the Python script each minute to take readings:
```
* * * * * python /home/pi/cron_jobs/sensor_sweep.py
```
