#!/usr/bin/env python
# -*- coding:utf-8 -*-

from commands import getoutput
import sys, re
from time import sleep

iface=sys.argv[1]

while 1:
	iwOut=getoutput("iw dev "+iface+" scan")

	res = re.compile('BSS ([\w\d\:]+).*\n.*\n.*\n.*\n.*\n\tsignal: ([-\.\d]+) dBm\n\tlast seen: (\d+) ms ago\n\tSSID: (.*)\n', re.MULTILINE).findall(iwOut)
	if len(res)!=len(re.compile('signal: ([-\.\d]+ dBm)\n', re.MULTILINE).findall(iwOut)): print "Problème !"
	if res:
		for x in res:
			print x
