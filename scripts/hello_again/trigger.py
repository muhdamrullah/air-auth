from __future__ import division
import smtplib
import os
import calendar
import time
import numpy as np
from astropy.io import ascii
import glob
import subprocess

def findPhone(mac_address):
    with open('../air-auth/database.csv') as dataBase:
        for line in dataBase:
	    column = line.split(', ')
	    if mac_address in line:
		return (column[2], column[1])

def writeFile():
    if os.path.isfile("./sent_list.dat"):
        print "There is a SENT file that exists..."
    else:
        ascii.write([ np.array([]), np.array([])], names=['mac','sent_time'], output='./sent_list.dat')

restricted_list = np.array(["00:26:75:BB:E9:40","F4:F2:6D:0E:D7:74","BC:6C:21:02:FC:49","A9:8E:24:68:98:80","69:94:23:A4:6F:23","8D:3A:E3:45:88:C7","88:53:2E:B3:CC:98", "48:E9:F1:2A:C1:E3", "A0:18:28:2A:0F:5C"])

def mainCommand():
    while True:    
        check_sent = glob.glob("./sent_list.*")
        if check_sent!=[]:
            sent_already = ascii.read("./sent_list.dat")
        else:
            sent_already = np.array([])

        if (os.path.isfile("./trigger.dat")):
            trigger_input = ascii.read("./trigger.dat", guess=False)
            if len(trigger_input['mac'])>0:
		additionalCondition = 1
		time.sleep(1)
                if len(sent_already["mac"])!=0:
		  try:
                    trig_unique_1 = np.array([x if ((x not in sent_already['mac'])|( (x in sent_already['mac'])and(np.max(sent_already['sent_time'][sent_already['mac']==x]) < calendar.timegm(time.gmtime()) - 10*60))) else "-99" for x in trigger_input['mac']])
                    trig_unique_2 = ((trig_unique_1[trig_unique_1!="-99"]))
                    print "Success"
		    print trig_unique_2
		    additionalCondition = 0
		  except Exception,e:
		    print str(e)
		    trig_unique_2 = np.array([])
		    print trig_unique_2
		    print "Pass3-Failed"
		   # print trig_unique_2
                else:
                    trig_unique_1 = trigger_input['mac']
                    trig_unique_2 = trig_unique_1
                    print "Initializing"
		    additionalCondition = 0

                if len(trig_unique_2)>0:
                    outbound_macs = np.array([])
                    outbound_time = np.array([])

                    for x in trig_unique_2:
                        if x not in restricted_list and additionalCondition == 0:
                            outbound_macs = np.append(outbound_macs, x)
                            outbound_time = np.append(outbound_time, (calendar.timegm(time.gmtime())) )
                            print_message = "Mac:%s, Last Visited:%s, Time Spent:%s minutes \n"%(x, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(trigger_input['last_seen'][trigger_input['mac']==x]+ 8*60*60 )) , (trigger_input['time_spent'][trigger_input['mac']==x]))
                            print print_message
			    time.sleep(1)
			    namewithNumber = findPhone(x)
			    if namewithNumber is None:
				whatsapp_message = './yowsup-cli demos -c file.config -M -s 6584983348 "%s"' % print_message 
			    else:
			        whatsapp_message = './yowsup-cli demos -c file.config -M -s 65%s "%s, have you registered for Balik Kampung?"' % namewithNumber
			    subprocess.call(whatsapp_message, shell=True)

                    if len(sent_already)==0:
                        ascii.write([outbound_macs, outbound_time], names=['mac','sent_time'], output='./sent_list.dat')
                    else:
                        ascii.write([np.append(sent_already['mac'], outbound_macs), np.append(sent_already['sent_time'],outbound_time)], names=['mac','sent_time'], output='./sent_list.dat')

while True:
    try:
        writeFile()
        mainCommand()
    except ValueError:
	pass
