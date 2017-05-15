# Home Automation Project
---
This project enables you to use a Raspberry Pi to record and log the relative humidity, barometric pressure, temperature, and event records. It is possible to implement the sensors, API, and database on one Raspberry Pi or spread it out among several (i.e. one pi running the database, another running the API, and as many others as you want running sensors).

## Set Up the Raspberry Pi
---

### Hardware
- Raspberry Pi 3 Model B (2.5 amp power supply, MicroUSB Cable, and MicroSD Card)
- BME280 Barometric Pressure, Relative Humidity, and Temperature Sensor
- SparkFun Beefcake Relay Control Kit Version 2.0
- Reed Switch

### Install Required Packages
   ```
   sudo apt-get install python-pip python-dev python-setuptools git
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
1. Install Postgres.
   ```
   sudo apt-get install postgresql postgresql-contrib libpq-dev
   ```
2. Log into Postgres.
   ```
   sudo -u postgres psql
   ```
3. Set a password for the postgres user.
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

## Set Up the Hub API
---

### Working with Flask
While developing with Flask it is possible to launch an application by executing the file. This app is launched ina development server - to deploy this in "production" takes an actual web server. This app, the home automation platform (REST API), will run in Apache version 2.4. Deploying in other versions of Apache will require changes to the home_automation_platform.conf file.

### Steps to Setting Up and Deploying in Apache and Flask
1. Install Apache web server, the WSGI module, and flask.
   ```
   sudo apt-get install apache2 python-flask libapache2-mod-wsgi
   ```
2. Install the psycopg2 library to interact with the database.
   ```
   sudo pip install psycopg2
   ```
3. Copy the home_automation_platform folder under the api folder in the repository into /var/www/. Edit the \_\_init\_\_.py file to add details about the database in the empty fields at the top of the file. 
4. Copy the home_automation_platform.conf file into /etc/apache2/sites-available/. Edit it with the IP or hostname of the server that will be running the api.
5. Open /etc/apache2/sites-available/000-default.conf and ensure that the virtual host is set to something besides port 80 since that is the port the app will run on.
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

## Set Up the Sensor
---

### Install Required Libraries
   ```
   sudo apt-get install python-requests python-smbus
   ```

### Set Up I2C
1. Edit /ect/modules and add this line.
   ```
   i2c-dev
   ```
   
2. Edit /boot/config.txt and add lines:
   ```
   dtparam=i2c_arm=on
   ```
   
3. Reboot the Raspberry Pi.
4. Connect the BME280 sensor to the GPIO ports and run the command
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
7. If this is an environment module make sure to update the BME280.py file with the i2c device address.

## Set Up the Node API

### Install Required Dependencies
1. Install Apache web server, the WSGI module, and flask.
   ```
   sudo apt-get install apache2 python-flask libapache2-mod-wsgi
   ```
2. Move the whichever node folder (e.g. garage_node, environment_node) to /var/www/.
3. Move the .conf file for the node into /etc/apache2/sites-available/.
4. Add the www-data user to the gpio and i2c groups. Without this step the user running apache will not be able to access the GPIO pins.
   ```
   sudo adduser www-data gpio
   sudo adduser www-data i2c
   ```
5. Open /etc/apache2/sites-available/000-default.conf and ensure that the virtual host is set to something besides port 80 since that is the port the app will run on.
   Original:
   ```
   <VirtualHost *:80>
   ```
   Change to:
   ```
   <VirtualHost *:8080>
   ```
6. Enable the site in apache. For example:
   ```
   sudo a2ensite environment_node.conf
   ```
7. Reload the `apache2` service.
   ```
   sudo service apache2 reload
   ```
