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
1. Edit /etc/wpa\_supplicant/wpa\_supplicant.conf and add lines:
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
3. Copy the home\_automation_platform folder under the api folder in the repository into /var/www/. Edit the \_\_init\_\_.py file to add details about the database in the empty fields at the top of the file. 
4. Copy the home\_automation_platform.conf file into /etc/apache2/sites-available/. Edit it with the IP or hostname of the server that will be running the api.
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
6. The command prints out connected devices. This example shows one BME280 connected:
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
7. Make sure to update the BME280.py file with the i2c device address.

## Set Up the Endpoint API
---

### Install Required Dependencies
Install Apache web server, the WSGI module, and flask.
   ```
   sudo apt-get install apache2 python-flask libapache2-mod-wsgi
   ```

### Copy Files and Set Permissions
1. Move the endpoint folder containing endpoint.wsgi to /var/www/. The folder structure should look like:
   ```
   /var/www/endpoint/endpoint.wsgi
   /var/www/endpoint/endpoint/\_\_init\_\_.py
   /var/www/endpoint/endpoint/api_sensors.py
   /var/www/endpoint/endpoint/api_garage.py
   /var/www/endpoint/endpoint/BME280.py
   ```
2. Move endpoint.conf into /etc/apache2/sites-available/.
3. Add the www-data user to the gpio and i2c groups to allow apache to access the GPIO pins and run the BME280 sensor.
   ```
   sudo adduser www-data gpio
   sudo adduser www-data i2c
   ```

### Remove Default Sites and Activate the API
1. Navigate to /etc/apache2/sites-available/ and delete 000-default.conf and default-ssl.conf.
2. Disable the default site in apache.
   ```
   sudo a2dissite 000-default.conf
   ```
3. Enable the endpoint api in apache. For example:
   ```
   sudo a2ensite endpoint.conf
   ```
4. Reload the `apache2` service.
   ```
   sudo service apache2 restart
   ```

## Security
---

### Set Up SSH Keys
Setting up SSH keys and turning off password authentication greatly inceases security surrounding SSH. Without the private key a user will not be able to SSH into the raspberry pi. 
1. Generate the key pair. Add whatever comment makes sense between the quotation marks. Add a password at the prompt if you want added security, and otherwise just hit enter to use it without a password. 
   ```
   ssh-keygen -t rsa -C "Home Automation Net"
   ```
2. There should be two files in the ~/.ssh folder: id\_rsa and id\_rsa.pub. Save these files somewhere safe.
3. The id_rsa file is the private key; only put this key in the .ssh folder on computers you want to use to SSH from. Do not allow anyone else to have the id\_rsa file. Once copied to a new machine the permissions need to be set as follows.
   ```
   sudo chmod 0644 ~/.ssh/id_rsa
   ```
4. Copy the contents of the id\_rsa.pub file, and add them to the ~/.ssh/authorized\_keys file on any Raspberry Pi you want to be able to SSH into using keys. 
5. Make sure this line is uncommented in the /etc/ssh/sshd\_config file.
   ```
   AuthorizedKeysFile      %h/.ssh/authorized_keys
   ```
6. In the /etc/ssh/sshd_config file uncomment this line and change yes to no to disable password authentication or simply add the line below to the file. 
   ```
   PasswordAuthentication no
   ```
7. Reload the ssh service. NOTE: Make sure the key pair is saved, the id_rsa file is in place where you will SSH from, and the public key has been copied to the ~/.ssh/authorized\_keys file on the destination. 
   ```
   sudo service apache2 reload
   ```
8. Place the public key on all the nodes. Place the private key on whichever computers you will use to SSH as well as the hub node.

### Set Up iptables
Iptables is the firewall packaged with Raspbian and it has wide open permissions by default. It has three chains: one for incoming, outgoing, and another for forwarded. We will use this to restrict access to the nodes, since everything will be centralized at the hub node. Make sure the same configuration is made on every node aside from the hub.
1. Ensure that there are no rules in place. If there are existing rules and policies ensure that they do not block the changes here. If nothing has been set up everything should be allowed by default.

Command:
   ```
   sudo iptables -L -v -n
   ```
Output:
   ```
   Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
   pkts bytes target     prot opt in     out     source               destination 

   Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
   pkts bytes target     prot opt in     out     source               destination 

   Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
   pkts bytes target     prot opt in     out     source               destination 
   ```
2. Set the policy to drop anything being forwarded. These are end nodes and don't need the ability to forward. 
   ```
   sudo iptables -P FORWARD DROP
   ```
3. Add permitted access for incoming communications. Use this command for each device that will be used to connect. Replace the IP address below with the IP address or hostname of the device you will connect from. NOTE: Make sure to include the hub node. 
   ```
   sudo iptables -A INPUT -s 192.168.1.10 -j ACCEPT
   ```
4. Add permitted access for the loopback address.
   ```
   sudo iptables -A INPUT -s 127.0.0.1 -j ACCEPT
   ```
5. Add permitted access for the loopback interface. 
   ```
   sudo iptables -A INPUT -i lo -j ACCEPT
   ```
6. By default iptables only writes changes to running memory, which is flushed on reboot. In order to make these firewall rules stick around, install iptables-persistent. As part of the install process it will ask to save the current rules. Select "yes" and hit enter for v4 and v6 rules.
   ```
   sudo apt-get install iptables-persistent
   ```
7. Add one final catch-all rule to reject any other communications not caught by the above rules.
   ```
   sudo iptables -A INPUT -j REJECT
   ```
8. The rules are saved to /etc/iptables/rules.v4 and /etc/iptables/rules.v6 by iptables-persistent, and then loaded from there on startup. In case changes must be made to the firewall rules, use iptables to change the rules to the desired configuration and then use iptables to save these changes to the file.
   ```
   sudo bash -c "iptables-save > /etc/iptables/rules.v4"
   ```
9. In the future, when running updates the catch-all deny rule must be disabled. The iptables rules can be displayed with line numbers; the rule can be deleted by line number. In this example the line number for the catch-all rule is 6.
   ```
   sudo iptables -L -v -n --line-numbers
   sudo iptables -D INPUT 6
   ```
10. Edit the ssh configuration file /etc/ssh/sshd_config and add this line. Without this line it will take longer to login via SSH because it will try to resolve the hostname.
   ```
   UseDNS no
   ```

### Set Up SSL for Apache
By enabling SSL in Apache all the web traffic to and from the nodes will be encrypted, as well as any traffic between a browser and the hub node. Part of the value of SSL certificates is in the trust that you got to the rigth server. Being able to see green whenever the console is accessed is a good indicator the real and correct website is being accessed. 
1. Choose hostnames for each node and set them by editing the /etc/hostname file. There should be one line at the top of the file; change this to the desired hostname. 
2. On the hub node edit the /etc/hosts file and add entries for each node. For example:
   ```
   127.0.0.1       localhost
   ::1             localhost ip6-localhost ip6-loopback
   ff02::1         ip6-allnodes
   ff02::2         ip6-allrouters
   
   127.0.1.1       automation-hub
   192.168.1.11    automation-db
   192.168.1.12    automation-office
   192.168.1.13    automation-backyard
   192.168.1.14    automation-garage
   ```
3. On each node aside from the database and hub, add an entry to the hosts file for the hub node.
   ```
   192.168.1.10    automation-hub
   ```
4. On each node: Make sure the entry in the hosts file for 127.0.1.1 matches the hostname set in /etc/hostname. Reboot each Raspberry Pi to apply the change.
5. Make the folder /etc/apache2/ssl to store the certificate file and the key file.
6. Run this command to generate the self-signed certificate and deposit the files in the right folder. At this point in the process it may be prudent to get certificates signed by a widely trusted certificate authority for the hub, rather than using self-signed certificates. 
   ```
   sudo openssl req -x509 -nodes -days 1095 -newkey rsa:2048 -out /etc/apache2/ssl/server.crt -keyout /etc/apache2/ssl/server.key
   ```
7. Activate the SSL module.
   ```
   sudo a2enmod ssl
   ```
8. The next step is to get the configuration loaded. This can either be done by replacing the contents of the original conf file in /etc/apache2/sites-available/ or by copying the conf file with -ssl appended to the name and then making that site available. Directions for that process are included in the set-up steps for Apache.
9. Restart the apache service.
   ```
   sudo service apache2 restart
   ```
10. Troubleshooting the apache configuration can be done with this command. It is useful if apache won't start.
   ```
   apachectl configtest
   ```
