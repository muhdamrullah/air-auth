from flask import Flask
from flask import request
from flask import render_template
import subprocess
import time

def createHotspot():
    subprocess.call('ifconfig wlan0 down', shell=True)
    time.sleep(1)
    subprocess.call('iwconfig wlan0 mode monitor', shell=True)
    time.sleep(1)
    subprocess.call('ifconfig wlan0 up', shell=True)
    time.sleep(1)
    subprocess.call('airbase-ng -e OpenWifi -c 6 wlan0', shell=True)
    time.sleep(60)
    subprocess.call('pkill airbase-ng', shell=True)
    time.sleep(1)

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
