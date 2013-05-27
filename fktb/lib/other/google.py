#!/usr/bin/env python
# -*- coding:utf-8 -*-

def geoloc(self):
    """Google Wi-Fi Positioning System"""

    import re
    import gtk
    import urllib2
    import simplejson
    from commands import getoutput
    from time import strftime, localtime

    from fktb.core.constants import FKTB_PATH, GOOGLE_API_KEY

    iface=self.combo_iface_geoloc.get_active_text().split()[0]

    if getoutput("which iwlist"):
    #     os_info=getoutput("uname -a").lower()
    #     alert="Un outils est nécessaire, veuillez l'installer :\niw - tool for configuring Linux wireless devices"
    #     alert+=''.join(["\n\n# apt-get install iw" for os in "backtrack","debian","ubuntu","mint","voyager" if os in os_info and not "apt-get" in alert])
    #     alert+=''.join(["\n\n# yum install iw\n(à vérifier)" for os in "fedora","centos" if os in os_info and not "yum" in alert])
    #     gtk.gdk.threads_enter()
    #     self.msgbox(alert,1)
    #     gtk.gdk.threads_leave()
    # else:
        self.btn_geoloc.set_sensitive(False)
        self.btn_geoloc.set_label("Scan des réseaux Wi-Fi à proximité ...")

        iwOut = getoutput("iwlist %s scanning" % iface)

        if "failed" in iwOut:
            if not self.statuGeolocLoop:
                self.statuGeolocLoop=False
                self.btn_geoloc.set_label("Lancer la géolocalisation")
                self.btn_geoloc.set_sensitive(True)
                gtk.gdk.threads_enter()
                self.msgbox("Le scan des réseaux Wi-Fi a échoué.\n\nVérifiez votre carte réseau sans fils !",1)
                gtk.gdk.threads_leave()
            else:
                self.btn_geoloc.set_label("Echec du scan, nouvel essai dans 5 secondes ...")
        else:
            result = re.compile("Address: ([\w\d\:]+)(?:.*\n)+?\s*Quality=[\d/]*\s*Signal level=([-\.\d]+) dBm", re.MULTILINE).findall(iwOut)

            self.btn_geoloc.set_label("Génération de la requête ...")

            # Old API
            # loc_req={ "version":"1.1.0",
            #           "request_address":False,
            #           #"addresults_language":"fr",
            #           "wifi_towers":[{"mac_address":x[0].replace(":","-"),"signal_strength":int(x[1])} for x in result]
            # }

            # loc_req = {
            #     "wifiAccessPoints": [
            #         {
            #             "macAddress": "01:23:45:67:89:AB",
            #             "signalStrength": -65,
            #             # "age": 0,
            #             # "channel": 11,
            #             # "signalToNoiseRatio": 40
            #         }
            #     ]
            # }

            loc_req = {
                "wifiAccessPoints": [{"macAddress":x[0],"signalStrength":int(x[1])} for x in result]
            }

            if len(result) < 2 :
                if not self.statuGeolocLoop:
                    self.statuGeolocLoop=False
                    self.btn_geoloc.set_label("Lancer la géolocalisation")
                    self.btn_geoloc.set_sensitive(True)
                    gtk.gdk.threads_enter()
                    self.msgbox("Nombre de points d'accès aux alentours insuffisant !", 1)
                    gtk.gdk.threads_leave()
                else:
                    self.btn_geoloc.set_label("Nombre de points d'accès aux alentours insuffisant, nouvel essai dans 5 secondes ...")

            print '\n'.join([l.rstrip() for l in simplejson.dumps(loc_req, sort_keys=True, indent=4*' ').splitlines()])

            if len(result) >= 2 :
                self.btn_geoloc.set_label("Envoi de la requête à Google ...")

                data = simplejson.JSONEncoder().encode(loc_req)
                print data
                try:
                    # Old API :
                    # https://www.google.com/loc/json
                    # New :
                    # https://www.googleapis.com/maps/api/geolocation/v1/geolocate
                    # https://www.googleapis.com/geolocation/v1/geolocate?key=
                    x = urllib2.urlopen('https://www.googleapis.com/geolocation/v1/geolocate?key=%s&sensor=false' % GOOGLE_API_KEY, data).read()
                    print "x: %s" % x
                    output = simplejson.loads(x)
                    print output
                except Exception as err:
                    print err
                    print err.args
                    print err.message
                    if not self.statuGeolocLoop:
                        self.statuGeolocLoop=False
                        self.btn_geoloc.set_label("Lancer la géolocalisation")
                        self.btn_geoloc.set_sensitive(True)
                        gtk.gdk.threads_enter()
                        self.msgbox("Impossible d'envoyer la requête :\nla connexion avec l'API Google a échoué.\n\nVérifiez votre connexion internet !",1)
                        gtk.gdk.threads_leave()
                    else: self.btn_geoloc.set_label("Echec de la requête vers l'API, nouvel essai dans 5 secondes")
                else:
                    pb = gtk.gdk.pixbuf_new_from_file_at_size("%s/images/icone.png" % FKTB_PATH, 24,24)
                    try:
                        self.osm.image_add(output["location"]["latitude"], output["location"]["longitude"], pb)
                        self.osm.set_center_and_zoom(output["location"]["latitude"], output["location"]["longitude"], 16)
                    except: pass
                    else:
                        self.liststore_geoloc.append(("["+strftime('%H:%M:%S', localtime())+"]", "longitude : "+str(output["location"]["longitude"])+", latitude : "+str(output["location"]["latitude"])))
                        if not self.statuGeolocLoop:
                            self.btn_geoloc.set_label("Lancer la géolocalisation")
                            self.btn_geoloc.set_sensitive(True)
                        else:
                            self.btn_geoloc.set_label("Ok, prochaine géolocalisation dans 5 secondes")