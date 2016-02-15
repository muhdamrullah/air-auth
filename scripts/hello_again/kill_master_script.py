import subprocess

subprocess.call('pkill -1 -f trigger.py', shell=True)
subprocess.call('pkill -1 -f database_lookup.py', shell=True)
subprocess.call('pkill -1 -f processed_stream.py', shell=True)
subprocess.call('pkill -1 -f live_stream.py', shell=True)
