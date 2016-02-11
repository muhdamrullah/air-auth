from flask import Flask
from flask import request
from flask import render_template
import subprocess
import time
import re
import csv

def createHotspot():
    subprocess.call('ifconfig wlan0 down', shell=True)
    time.sleep(1)
    subprocess.call('iwconfig wlan0 mode monitor', shell=True)
    time.sleep(1)
    subprocess.call('ifconfig wlan0 up', shell=True)
    time.sleep(1)
    subprocess.Popen('airbase-ng -e OpenWifi -c 6 wlan0 >> test.csv', shell=True)
    time.sleep(10)
    searchMAC()
    subprocess.call('pkill airbase-ng', shell=True)
    time.sleep(1)

def searchMAC():
    for x in range (0,11):
        with open('test.csv','rb') as myFile:
            myFile.seek(-200,2)
            last = myFile.readlines(1)[-1].decode()
            searchFilter = 'Client'
	    if searchFilter in last:
                result = re.search("Client (.*) associated", last)
                print result.group(1)
	        time.sleep(5)
	        break
	    else:
	        time.sleep(5)

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    processed_text = text.upper()
    createHotspot()
    return processed_text

if __name__ == '__main__':
    app.run(debug=True)
