#!/usr/bin/env python
# -*- coding:utf-8 -*-

def wifiView(self):
    from commands import getoutput
    import re
    import gtk
    import thread
    from time import sleep

    iface=self.combo_iface_wifi.get_active_text().split()[0]

    if self.enCoursWifi:
        self.enCoursWifi=0
        self.btn_wifi.set_label("Start")
    elif "(-19)" in getoutput("iw "+iface+" info"):
        gtk.gdk.threads_enter()
        self.btn_wifi.set_label("Start")
        self.msgbox("Veuillez sélectionner une interface Wi-Fi !",1)
        gtk.gdk.threads_leave()
        self.enCoursWifi=0
    else:
        self.enCoursWifi=1
        thread.start_new_thread(self.runProgressbarWifi, ())
        self.btn_wifi.set_label("Stop")
        self.progressbarWifi.set_text("Scan en cours ...")

        rssiMin=-120
        rssiMax=-30
        while self.enCoursWifi:
            iwOut=getoutput("iwlist %s scanning" % iface)

            if not iwOut:
                continue
            if "Network is down" in iwOut:
                gtk.gdk.threads_enter()
                self.btn_wifi.set_label("Start")
                self.msgbox("L'interface Wi-Fi séléctionnée est désactivée !",1)
                gtk.gdk.threads_leave()
                self.enCoursWifi=0
            else:
                # BSS ([\w\d\:]+)(?:.*\n)+?\tsignal: ([-\.\d]+) dBm\n\tlast seen: (\d+) ms ago\n\tSSID: (.*)\n
                res = re.compile('Address: ([\w\d\:]+)(?:.*\n)+?\s*Quality=[\d/]*\s*Signal level=([-\.\d]+) dBm\s*\n.*\n\s*ESSID:"(.*)"', re.MULTILINE).findall(iwOut)
                if len(res)!=len(re.compile('Signal level=([-\.\d]+) dBm', re.MULTILINE).findall(iwOut)):
                    print "Problème !"

                for x in res:
                    found=0
                    apIter=self.liststore_wifi.get_iter_first() # None quand liststore vide
                    while apIter:
                        if self.liststore_wifi.get_value(apIter, 1) == x[0]:
                            self.liststore_wifi.set(apIter, 2, x[1], 3, int((float(x[1])-rssiMin))*100/(rssiMax-rssiMin)) # Modifier une ligne
                            # if int(x[2])>5000: self.liststore_wifi.set(apIter, 2, '', 3, 0) # Modifier une ligne
                            found=1
                        apIter=self.liststore_wifi.iter_next(apIter)
                    else:
                        if not found:
                            self.liststore_wifi.append([x[2],x[0],x[1],int((float(x[1])-rssiMin))*100/(rssiMax-rssiMin)])
            sleep(1)