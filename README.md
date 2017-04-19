# Home Automation Project
---
Driver code for the BMP085 and DHT22 sensors originated from Adafruit and has not been modified. For more information on setting up these sensors, please visit the Adafruit website. When properly implemented this project enables you to use a Raspberry Pi to record and log the relative humidity, barometric pressure, temperature, and event records. It is possible to implement the sensors, API, and database on one Raspberry Pi or spread it out among several (i.e. one pi running the database, another running the API, and as many others as you want running sensors).

## Set Up the Raspberry Pi
---

### Required Hardware
- Raspberry Pi 3 Model B
- 2.5 amp power supply
- MicroUSB Cable
- MicroSD Card
- DHT22 Humidity and Temperature Sensor
- BMP085 Barometric Pressure and Temperature Sensor
- Breadboard
- Breadboard Jumper Wires (Male-to-Male)
- Breadboard Jumper Wires (Female-to-Male)
- 4.7k Ohm Resistor for DHT22 Sensor

### Install Required Packages
   ```
   sudo apt-get install python-pip python-dev python-setuptools python-smbus libpq-dev postgresql postgresql-contrib git
   ```

### Run raspi-config Utility
The raspi-config utility can be run with the comman `sudo raspi-config`. It will allow you to set the timezone, locale, and many other things.

### Add WiFi Credentials to the Supplicant File (Optional)
1. Edit /etc/wpa_supplicant/wpa_supplicant.conf and add lines:
   ```
   network={
	   ssid="network name here"
	   psk="network password here"
   }
   ```
2. Take WiFi offline.
   ```
   sudo ifdown wlan0
   ```
3. Put WiFi back online.
   ```
   sudo ifup wlan0
   ```

## Set Up PostgreSQL
---

### Prepare PostgreSQL
1. Log into Postgres.
   ```
   sudo -u postgres psql
   ```
2. Set a password for the postgres user.
   ```
   ALTER USER postgres WITH PASSWORD 'your password here';
   ```

### Allow Remote Database Access from the API Host
1. Edit the file /etc/postgresql/9.4/main/pg_hba.conf and add the line below to restrict database access to the postgres user and the REST API host (hostname or ip address with cidr). 
   ```
   host    all     postgres     192.168.1.5/24       md5
   ```
   
2. Edit the file /etc/postgresql/9.4/main/postgresql.conf and uncomment or add this line:
   ```
   listen_addresses = '*'
   ```

### Create the Database and Schema
1. Run the database setup script using the psql utility to generate the database, generate its tables, and fill them with some initial data:
   ```
   psql -h [DB SERVER HOSTNAME/IP] -U postgres -p 5432 -f db_creation_script.sql
   ```

## Set Up the RESTful API
---

### Working with Flask
While developing with Flask it is possible to launch an application by executing the file. This app is launched ina development server - to deploy this in "production" takes an actual web server. This app, the home automation platform (REST API), will run in Apache version 2.4. Deploying in other versions of Apache will require changes to the home_automation_platform.conf file.

### Steps to Setting Up and Deploying in Apache and Flask
1. Install Apache web server, the WSGI module, and flask.
   ```
   sudo apt-get install apache2 python-flask libapache2-mod-wsgi
   ```
2. Install the psycopg2 library to interact wit hthe database.
   ```
   sudo pip install psycopg2
   ```
3. Copy the home_automation_platform folder under the api folder in the repository into /var/www/. This includes the WSGI configuration file and the __init__ file with the code running the API. You must edit the __init__.py file to add details about the database in the fileds with empty strings at the top of the file. 
4. Copy the home_automation_platform.conf file into /etc/apache2/sites-available/. This is the apache configuration file, and you must edit it with the IP or hostname of the server that will be running the api.
5. Open /etc/apache2/sites-available/default and ensure that the virtual host is set to something besides port 80 since that is the port the app will run on.
   Original:
   ```
   <VirtualHost *:80>
   ```
   Change to:
   ```
   <VirtualHost *:8080>
   ```
6. Enable the site in apache.
   ```
   sudo a2ensite home_automation_platform.conf
   ```
7. Reload the `apache2` service.
   ```
   sudo service apache2 reload
   ```
8. At this point the app should be running and handling requests. Try testing it by using curl to send it some information. 
   For Example:
   ```
   curl -H "Content-Type: application/json" -X POST -d '[ {"value":72, "unit_id":1}, {"value":990, "unit_id":2}, { "value":60, "unit_id":3} ]' http://192.168.1.200/sensor_records/1

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
4. Connect the BMP085 sensor to the GPIO ports and run the command
   ```
   sudo i2cdetect -y 1
   ```
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

### Set Up the DHT22 Driver
1. Navigate to the folder with the DHT22 driver code:
`cd Adafruit_Python_DHT/`
2. Run the script to install the driver:
`sudo python setup.py install`
3. Navigate to the examples folder inside the Adafruit_Python_DHT folder:
`cd examples/`
4. Edit the `simpletest.py` file and ensure the sensor and pin are set correctly.
5. Run the `simpletest.py` file and ensure that sensor readings are returned.

### Set Up a Cronjob to Run the Script Gathering Sensor Readings
1. Edit the cronjob file.
   ```
   sudo crontab -e
   ```
2. Add this line to execute the Python script each hour on the hour.
   ```
   0 * * * * python /home/pi/cron_jobs/sensor_sweep.py
   ```
