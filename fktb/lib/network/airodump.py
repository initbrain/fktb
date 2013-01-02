#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, re
from time import sleep

import csv

file=sys.argv[1]

while 1:
	with open(file, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if row:
				if len(row) == 15 and row[0] != "BSSID": # grande ligne
					print "BSSID           : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[0]))
					print "First time seen : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[1]))
					print "Last time seen  : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[2]))
					print "channel         : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[3]))
					print "Speed           : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[4]))
					print "Privacy         : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[5]))
					print "Cipher          : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[6]))
					print "Authentication  : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[7]))
					print "Power           : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[8]))
					print "# beacons       : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[9]))
					print "# IV            : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[10]))
					print "LAN IP          : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[11]))
					print "ID-length       : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[12]))
					print "ESSID           : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[13]))
					print "Key :           : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[14]))
				elif len(row) == 7 and row[0] != "Station MAC": # petite ligne
					print "Station MAC     : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[0]))
					print "First time seen : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[1]))
					print "Last time seen  : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[2]))
					print "Power           : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[3]))
					print "# packets       : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[4]))
					print "BSSID           : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[5]))
					print "Probed ESSIDs   : "+re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[6]))+"\n"
	sleep(1)


###


	sudo airodump-ng mon0 --write "fktb_path+"/airodump_ng_dump.csv --output-format csv -u 1"

        commands.getstatusoutput("airodump-ng --write /tmp/fern-log/zfern-wep --output-format csv \
                                    --encrypt wep %s"%(monitor))          #FOR WEP
        

        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall airmon-ng')

                #
                # Create Fake Mac Address and index for use
                #
                mon_down = commands.getstatusoutput('ifconfig %s down'%(mon_real))
                set_fake_mac = commands.getstatusoutput('macchanger -A %s'%(mon_real))
                mon_up = commands.getstatusoutput('ifconfig %s up'%(mon_real))
                mac_str = str(commands.getstatusoutput('ifconfig'))
                mac_index = mac_str.index(mon_real)
                mac_address = mac_str[mac_index+36:mac_index+36+17].replace('-',':')


