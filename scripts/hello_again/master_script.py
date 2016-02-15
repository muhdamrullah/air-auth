import subprocess
import os

FNULL = open(os.devnull, 'w')
subprocess.Popen('python live_stream.py', shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
subprocess.Popen('python processed_stream.py', shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
subprocess.Popen('python database_lookup.py', shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
subprocess.Popen('python trigger.py', shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
