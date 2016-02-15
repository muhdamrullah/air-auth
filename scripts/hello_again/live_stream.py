from astropy.io import ascii
import numpy as np
import datetime
import time
from time import strftime
import sys
import os
import glob
import calendar

def convert_epoch(x):
    t = (datetime.datetime( int((x.split(" ")[0]).split("-")[0]),  int(x.split(" ")[0].split("-")[1]),  int(x.split(" ")[0].split("-")[2]), int(x.split(" ")[1].split(":")[0]) ,   int(x.split(" ")[1].split(":")[1])  , int(x.split(" ")[1].split(":")[2])))
    return calendar.timegm(t.timetuple())

def convert_time(arr):
    return np.array([convert_epoch(x) for x in np.array(arr)])

def cat_string(list_of_files):
    if len(list_of_files)==0:
        iterator = np.array([])
    elif len(list_of_files)==1:
        iterator=list_of_files
    elif len(list_of_files)>=2:
        iterator = list_of_files[-2:]

    output=""
    for x in range(0, len(iterator)):
        output = output+iterator[x]+" "
    return output[:-1]


while True:

    try:

        raw1_file_list = glob.glob("../Raw/*.csv")
        raw2_file_list= np.array([x.split("/")[2] if "kismet" not in x else "-99" for x in raw1_file_list])
        raw3_file_list = raw2_file_list[raw2_file_list!="-99"]
        index_file_list = np.array([int(((x.split("-")[1]).split("."))[0]) for x in raw3_file_list])
        file_list= np.array([y[1] for y in sorted(zip(index_file_list, raw3_file_list),key=lambda x:x[0])])
        os.chdir("../Raw/")
        os.system("cat %s > ../Hello_Again/onelevel/real_time_combined_R.csv"%(cat_string(file_list)))
        os.chdir("../Hello_Again/")

        with open('./onelevel/real_time_combined_R.csv','r') as in_file, open('./onelevel/full_day_R.csv','w') as out_file:
            switch = 0
            out_file.write("Station MAC, First time seen, Last time seen, Power, # packets, BSSID \r")
            for line in in_file:
                if (line[0:5]=="Stati"):
                    switch = 1
                if (line[0]=="\r"):
                    switch = 0
                if switch==1:
                    if line[0]!="\r":
                        if (line.split(",")[0]!="Station MAC"):
                            processed_line = line.split(",")[0]+","+ line.split(",")[1]+","+line.split(",")[2]+","+line.split(",")[3]+","+line.split(",")[4]+","+line.split(",")[5]+"\r"
                            out_file.write(processed_line)


        raffles = ascii.read("./onelevel/full_day_R.csv")

        current_time = (calendar.timegm(time.gmtime()))
     
        #ascii.write([np.unique(raffles['Station MAC'][(calendar.timegm(time.gmtime()) + 8*60*60 - convert_time(raffles['Last time seen']))<70])], names=['macs'], output='./live_stream.dat')
        ascii.write([np.unique(raffles['Station MAC'][(calendar.timegm(time.gmtime()) - convert_time(raffles['Last time seen']))<70])], names=['macs'], output='./live_stream.dat')
        time.sleep(1)
        print "up and running"

    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print "live_stream fucked...now how?"
        pass
