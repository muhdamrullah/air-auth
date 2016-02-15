from astropy.io import ascii
import numpy as np
import datetime
import time
from time import strftime
import sys
import os
import glob
import calendar

while True:
    try:
        
        database = ascii.read("local_database.dat")
        live= ascii.read("live_stream.dat")

        current = np.array(live["macs"])
        archive = np.array(database["mac_by_session"])
        last_seen = np.array(database["last_seen"])
        first_seen = np.array(database["first_seen"])

        #archive_mask = np.array([1 if ((x in current)& (np.min(first_seen[database["mac_by_session"]==x]) < calendar.timegm(time.gmtime()) - 12*60*60 )) else 0 for x in archive], dtype=bool)
        archive_mask = np.array([1 if ((x in current)& (np.min(first_seen[database["mac_by_session"]==x]) < calendar.timegm(time.gmtime()) - 10*60 )) else 0 for x in archive], dtype=bool)

        keystone= zip(archive[archive_mask], last_seen[archive_mask], (last_seen[archive_mask] - first_seen[archive_mask])/60)

        sorted_k = sorted(keystone,key = lambda x:x[1])

        sorted_1 = (np.array([x[0] for x in sorted_k]))[::-1]
        sorted_2 = (np.array([x[1] for x in sorted_k]))[::-1]
        sorted_3 = (np.array([x[2] for x in sorted_k], dtype=int))[::-1]

        fin_1, places = np.unique(sorted_1, return_index=True)    
        
        ascii.write([fin_1, sorted_2[places], sorted_3[places]], names=['mac', 'last_seen', 'time_spent'], output='./trigger.dat')
        print "Success!!!"

    except (KeyboardInterrupt, SystemExit):
        raise
    except ValueError:
	print "Database_lookup f**k*d"	 
        pass
