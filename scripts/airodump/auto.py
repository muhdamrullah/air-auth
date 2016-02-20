#!/usr/bin/python

import subprocess
import time

while True:
  subprocess.Popen('sudo airodump-ng wlan0 -w dump', shell=True)
  time.sleep(900)
  subprocess.call('sudo pkill airodump-ng', shell=True)
