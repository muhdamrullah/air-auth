from flask import render_template
import subprocess
import time
import re
import csv
import datetime

def createHotspot():
    subprocess.call('ifconfig wlan0 down', shell=True)
    time.sleep(1)
    subprocess.call('iwconfig wlan0 mode monitor', shell=True)
    time.sleep(1)
    subprocess.call('ifconfig wlan0 up', shell=True)
    time.sleep(1)
    subprocess.Popen('airbase-ng -e Authentication -c 6 wlan0 >> test.csv', shell=True)
    time.sleep(10)
    return searchMAC()
    time.sleep(1)

def searchMAC():
    for x in range (0,11):
        with open('test.csv','rb') as myFile:
            myFile.seek(-200,2)
            last = myFile.readlines(1)[-1].decode()
            searchFilter = 'Client'
	    if searchFilter in last:
                result = re.search("Client (.*) associated", last)
                return result.group(1)
	        time.sleep(5)
	        break
	    else:
	        time.sleep(5)

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

    name_id = request.form['username']
    phone_id = request.form['password']
    mac_address = createHotspot()
    time_stamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    subprocess.call('pkill airbase-ng', shell=True)
    global dataBase
    dataBase = "%s, %s, %s, %s" % (time_stamp, name_id, phone_id, mac_address)
    saveDatabase()
    return render_template("result.html",
			    NAME=name_id,
			    PHONE=phone_id,
			    MAC_ID=mac_address)

if __name__ == '__main__':
    dataBase=""
    app.debug = True
    app.run('192.168.1.196', 8080)
