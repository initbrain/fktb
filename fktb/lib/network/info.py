# -*- coding: utf-8 -*-

import re
from commands import getoutput

# Récupérer les interfaces réseaux sans-fil (wireless) actives

def getWIface():
    result = Result()
    res = re.compile("^([\w\d]+).*?IEEE.*?\n", re.MULTILINE).findall(getoutput("iwconfig"))

    if len(res) > 0:
        return result.add(res)
    else:
        print "Aucune interface réseau sans-fil (wireless) détectée !"


def ifaceInfo():
    res = re.compile("^([\w\d]+).*?\n.*?inet adr:([\w\d\.]+)\s+Bcast:[\w\d\.]+\s+Masque:([\w\d\.]+)",
        re.MULTILINE).findall(getoutput("ifconfig"))

    if len(res) > 0:
        infos = {}
        for interface in res:
            binIp = [i for i in ''.join(
                '0' * (8 - len(i)) + i for i in [bin(int(octet))[2:] for octet in interface[1].split('.')])]
            binMask = [i for i in ''.join(
                '0' * (8 - len(i)) + i for i in [bin(int(octet))[2:] for octet in interface[2].split('.')])]
            netAddr = [str(int(binIp[i]) and int(binMask[i])) for i in range(32)]
            netAddr = '.'.join(str(int(''.join(netAddr[i * 8:i * 8 + 8]), 2)) for i in range(4))
            netBroadcast = [str(int(binIp[i]) or int(not(int(binMask[i])))) for i in range(32)]
            netBroadcast = '.'.join(str(int(''.join(netBroadcast[i * 8:i * 8 + 8]), 2)) for i in range(4))
            # print "Interface : "+interface[0]+"\nAdresse IP : "+interface[1]+"\nMasque du réseau : "+interface[2]+"\nAdresse du réseau : "+netAddr+"\nAdresse de broadcast : "+netBroadcast
            infos[interface[0]] = interface[1], netAddr, netBroadcast
        return infos
    else: return 0


def main():
    print getWIface()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print err