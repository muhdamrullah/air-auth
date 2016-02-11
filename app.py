from flask import Flask
from flask import request
from flask import render_template
import subprocess
import time
import re
import csv
import datetime

# Create a temporary AP to harvest MAC Address
def createHotspot():
    # Set the interface to monitor mode
    subprocess.call('ifconfig wlan0 down', shell=True)
    time.sleep(1)
    subprocess.call('iwconfig wlan0 mode monitor', shell=True)
    time.sleep(1)
    subprocess.call('ifconfig wlan0 up', shell=True)
    time.sleep(1)
    # Start the airbase-ng command with the Wi-Fi called 'Authenticate'
    subprocess.Popen('airbase-ng -e Authenticate -c 6 wlan0 >> test.csv', shell=True)
    time.sleep(10)
    return searchMAC()
    time.sleep(1)

# Search the MAC address within a csv file
def searchMAC():
    # Sets a 60 second loop for user to authenticate with the Wi-Fi
    for x in range (0,11):
        with open('test.csv','rb') as myFile:
            myFile.seek(-200,2)
	    # Search for the last line in the file to see if matches the filter
            last = myFile.readlines(1)[-1].decode()
            searchFilter = 'Client'
	    if searchFilter in last:
                result = re.search("Client (.*) associated", last)
                return result.group(1)
	        time.sleep(5)
	        break
	    else:
	        time.sleep(5)

# Save the pulled contents from form into a CSV file
def saveDatabase():
    myFile = open('database.csv','a')
    global dataBase
    myFile.write(dataBase)
    myFile.close()
    
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    # Variables from the form is given by request.form['variable']
    name_id = request.form['username']
    phone_id = request.form['password']
    mac_address = createHotspot()
    time_stamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    # To kill the AP for security purposes
    subprocess.call('pkill airbase-ng', shell=True)
    global dataBase
    dataBase = "%s, %s, %s, %s\n" % (time_stamp, name_id, phone_id, mac_address)
    # Authentication and verification to make sure fields are inputted correctly
    if len(phone_id) == 8 and phone_id.isdigit() and mac_address:
	saveDatabase()
	return render_template("result.html",
			    NAME=name_id,
			    PHONE=phone_id,
			    MAC_ID=mac_address)
    else:
	return render_template("index.html",
			    PHONE=phone_id)

# Main command to run on the local IP: 192.168.1.196 and port: 8080. 
if __name__ == '__main__':
    dataBase=""
    app.debug = True
    app.run('192.168.1.196', 8080)
