# -*- coding:utf-8 -*-
# Julien Deudon (initbrain) & Geoffrey Robert (mks)
# Free-knowledge Toolbox v0.2.3 du 20/06/2012

# Gestion des importations

import_error = ""                                # Variable de stockage des erreurs d'importation

import smtplib                                # <-
from email.MIMEMultipart import MIMEMultipart                #  |
from email.MIMEBase import MIMEBase                    #  Module utilisés pour l'envoi de mail
from email.MIMEText import MIMEText                    #  |
from email.Utils import COMMASPACE, formatdate                #  |
from email import Encoders

# Modules utilisés pour l'interface graphique
try:
    import pygtk
except ImportError:
    import_error += "\npygtk 2.3.90 ou ultérieur"
try:
    import gtk
except ImportError:
    import_error += "\ngtk"
else:
    if gtk.pygtk_version < (2, 3, 90) and import_error == "":
        import_error += "\npygtk 2.3.90 ou ultérieur"

try: import httplib2                            # Module utilisé pour effectuer des requêtes HTTP
except ImportError: import_error += "\nhttplib2"
try: import Image                            # Module utilisé par le module Couche RVB (stéganographie)
except ImportError: import_error += "\nPIL (Image)"
try: import re                                # Module utilisé pour le parsage (expressions rationnelles)
except ImportError: import_error += "\nre"
try: import webbrowser                            # Module permettant d'ouvrir le navigateur web
except ImportError: import_error += "\nwebbrowser"
try: from commands import getoutput, getstatusoutput            # Module utilisé pour récupérer la sortie d'une commande
except ImportError: import_error += "\ncommands"
try: import hashlib                            # Module utilisé pour le hashage de textes ou fichiers
except ImportError: import_error += "\nhashlib"
try: import thread                            # Module pour le multithreading
except ImportError: import_error += "\nthread"
try: import subprocess                            # Module permettant de créer des sous-processus
except ImportError: import_error += "\nsubprocess"
try: from urllib import urlencode                    # Module utilisé pour encoder des paramètres dans une URL
except ImportError: import_error += "\nurllib"
try: import urllib2                            # Module utilisé pour envoyer des requete aux API Google
except ImportError: import_error += "\nurllib2"
try: from time import *                            # Modules pour la vitesse du mouvement de la progressbar et
except ImportError: import_error += "\ntime"                # le calcul du temps pris par un traitement

try: import os                                # Module utilisé pour éxecuter des commandes
except ImportError: import_error += "\nos"                # et récupérer des informations d'environnement

try: import pynotify                            # Module utilisé pour afficher des notifications
except ImportError: import_error += "\npython-notify"

try: import simplejson                            # <-
except ImportError: import_error += "\nsimplejson"            #  |
try: import sys                                #  |
except ImportError: import_error += "\nsys"                #  Modules utilisés pour la géolocalisation
try: import os.path                            #  |
except ImportError: import_error += "\nos.path"                #  |
try: import gobject                            #  |
except ImportError: import_error += "\ngobject"                # <-

try:
    #Try static lib first
    mydir = os.path.dirname(os.path.abspath(__file__))
    libdir = os.path.abspath(os.path.join(mydir, "..", "python", ".libs"))
    sys.path.insert(0, libdir)

    import osmgpsmap                        # Module utilisé pour afficher une OpenStreetMap
except ImportError: import_error += "\nosmgpsmap"
#else: print "Utilisation de osmgpsmap : %s (version %s)" % (osmgpsmap.__file__, osmgpsmap.__version__)

try: import csv                                # Module utilisé pour lire les logs de airodump-ng
except ImportError: import_error += "\ncsv"

# Gestion des éventuelles erreurs d'importation

if import_error != "":
    print "Il est nécessaire de posséder les librairies suivantes pour faire fonctionner cette boîte à outils :" + import_error
    raise SystemExit

# Configurations

from fktb.core.constants import FKTB_PATH, CONFIG_PATH

gtk.gdk.threads_init() # Important : initialisation pour l'utilisation de threads
gtk.gdk.threads_enter()

class toolbox:

# Recherche de mise à jour

    # def checkUpdate(self, param=None):
    #     """Vérifie les mises à jour
    #     Parse le site google code pour récupérer la version la plus récente
    #     et la compare avec la version actuellement utilisée.
    #     """
    #     msg=''
    #     type_msg=0
    #     version = "0.2.3"
    #     cnx = httplib2.Http()
    #     try: ret = self.requete_http(cnx, "GET", "http://code.google.com/p/initbrain-toolbox/")
    #     except: msg,type_msg="Impossible de rechercher les mises à jour :\nla connexion à Google Code a échoué.",1
    #     else:
    #         res = re.compile('itemprop="description">v(.+) - NOUVEAU NOM : free-knowledge toolbox !</span>', re.MULTILINE).findall(ret)
    #         if not res: msg,type_msg="Impossible de rechercher les mises à jour :\nproblème avec la récupération de la version actuelle.",1
    #         else:
    #             for indice_ver in range(0,3):
    #                 if version.split('.')[indice_ver] < res[0].split('.')[indice_ver]:
    #                     msg="Une version plus récente est disponible !\n\nVersion utilisée : "+version+"\nVersion actuelle : "+res[0]+"\n\nRendez-vous sur :\nhttp://code.google.com/p/initbrain-toolbox/"
    #                     break
    #                 elif version.split('.')[indice_ver] > res[0].split('.')[indice_ver]:
    #                     msg="Vous disposez d'une prerelease ^^\n\nVersion officielle : "+res[0]+"\nVersion utilisée : "+version
    #                     break
    #                 elif indice_ver==2: msg="Pas de mises à jour disponibles.\n\nVersion actuelle : "+res[0]
    #
    #     # Bloquer la boucle principale juste le temps d'afficher une alerte
    #     # Exemple : http://aruiz.typepad.com/siliconisland/2006/04/threads_on_pygt.html
    #     gtk.gdk.threads_enter()
    #     self.msgbox(msg,type_msg)
    #     gtk.gdk.threads_leave()

# Récupérer les interfaces réseaux sans-fil (wireless) actives

    def getWIface(self):
        res=re.compile("^([\w\d]+).*?IEEE.*?\n", re.MULTILINE).findall(getoutput("iwconfig"))

        if len(res)>0:
            [self.combo_iface_wifi.append_text(iface) for iface in res]
            [self.combo_iface_wifi2.append_text(iface) for iface in res]
            [self.combo_iface_geoloc.append_text(iface) for iface in res]
            self.combo_iface_wifi.set_active(0)
            self.combo_iface_wifi2.set_active(0)
            self.combo_iface_geoloc.set_active(0)
        else: print "Aucune interface réseau sans-fil (wireless) détectéé !"

    def ifaceInfo(self):
        res=re.compile("^([\w\d]+).*?\n.*?inet adr:([\w\d\.]+)\s+Bcast:[\w\d\.]+\s+Masque:([\w\d\.]+)", re.MULTILINE).findall(getoutput("ifconfig"))

        if len(res)>0:
            infos={}
            for interface in res:
                binIp=[i for i in ''.join('0'*(8-len(i))+i for i in [bin(int(octet))[2:] for octet in interface[1].split('.')])]
                binMask=[i for i in ''.join('0'*(8-len(i))+i for i in [bin(int(octet))[2:] for octet in interface[2].split('.')])]
                netAddr=[str(int(binIp[i]) and int(binMask[i])) for i in range(32)]
                netAddr='.'.join(str(int(''.join(netAddr[i*8:i*8+8]),2)) for i in range(4))
                netBroadcast=[str(int(binIp[i]) or int(not(int(binMask[i])))) for i in range(32)]
                netBroadcast='.'.join(str(int(''.join(netBroadcast[i*8:i*8+8]),2)) for i in range(4))
                # print "Interface : "+interface[0]+"\nAdresse IP : "+interface[1]+"\nMasque du réseau : "+interface[2]+"\nAdresse du réseau : "+netAddr+"\nAdresse de broadcast : "+netBroadcast
                infos[interface[0]]=interface[1],netAddr,netBroadcast
            return infos
        else: return 0

# Threading

    def mkThreadMd5(self, parent):
        """Démarre un thread pour la fonction checkmd5_online"""
        t_md5 = thread.start_new_thread(self.checkmd5_online, ())

    def runProgressbarMd5(self):
        """Gérrer l'état de la progressbar du module "Recherche MD5" """
        while self.enCoursMd5:
            self.progressbarMd5.pulse()
            sleep(0.1)

        gtk.gdk.threads_leave() # Arret du thread

    def runProgressbarWifi(self):
        """Gérrer l'état de la progressbar du module Wi-Fi """
        while self.enCoursWifi:
            self.progressbarWifi.pulse()
            sleep(0.1)

        self.progressbarWifi.set_fraction(0)
        self.progressbarWifi.set_text("En attente ...")

        gtk.gdk.threads_leave() # Arret du thread

    def runProgressbarWifi2(self):
        """Gérrer l'état de la progressbar du module Wi-Fi 2 """
        while self.enCoursWifi2:
            self.progressbarWifi2.pulse()
            sleep(0.1)

        # Vérification des permissions
        for su_gui_cmd in ['gksu','kdesu','ktsuss','beesu','']:
            if getoutput("which "+su_gui_cmd): break
        if not su_gui_cmd:
            gtk.gdk.threads_enter()
            self.msgbox("Un des outils suivant est nécessaire pour acquérir les droits administrateur, veuillez en installer un :\n\ngksu\nkdesu\nktsuss\nbeesu",1)
            gtk.gdk.threads_leave()
        else: getstatusoutput(su_gui_cmd+" 'killall airodump-ng'")

        if os.path.exists("%s/tmp/airodump-ng-01.csv" % FKTB_PATH):
            os.remove("%s/tmp/airodump-ng-01.csv" % FKTB_PATH)

        self.progressbarWifi2.set_fraction(0)
        self.progressbarWifi2.set_text("En attente ...")

        gtk.gdk.threads_leave() # Arret du thread

    def mkThreadMail(self, parent):
        """Démarre un thread pour la fonction envoyer_mail"""

        # Récupération de la date d'envoi
        date_envoi_mail = self.entry_mail_date.get_text()
        if not date_envoi_mail: t_mail = thread.start_new_thread(self.envoyer_mail, (formatdate(localtime=True),))
        else:
            try: date_envoi_mail = formatdate(mktime(strptime(date_envoi_mail,"%d-%m-%Y %H:%M:%S")), True)
            except: self.warnDialog("Format de date incorrect !\n\nFormat : JJ-MM-AAAA hh:mm:ss\nex : 24-12-2012 03:13:37")
            else: t_mail = thread.start_new_thread(self.envoyer_mail, (date_envoi_mail,))

    def runProgressbarMail(self):
        """Gérrer l'état de la progressbar du module "Mail Anonyme" """
        while self.enCoursMail == 1 :
            self.progressbarMail.pulse()
            sleep(0.1)

        gtk.gdk.threads_leave() # Arret du thread

    def mkThreadSum(self):
        """Démarre un thread pour la fonction sumfile"""
        t_sum = thread.start_new_thread(self.sumfile, ())

# CESAR

    def chiffrement(self, texte, cle, alphabet):
        """Fonction éffectuant un chiffrement César"""
        cesar=""
        for lettre in texte:
            position=alphabet.find(lettre) # Position avant cryptage cesar, ex : alphabet.find('z') = 25
            if position != -1:
                position=position+cle
                while position >= len(alphabet):
                    position=position-len(alphabet)
                cesar=cesar+alphabet[position]
            elif alphabet.upper().find(lettre) != -1: # Si la lettre est une majuscule
                position=alphabet.find(lettre.lower())
                position=position+cle
                while position >= len(alphabet):
                    position=position-len(alphabet)
                cesar=cesar+alphabet[position].upper()
            else: # Si la lettre n'est pas dans l'alphabet on la laisse telle qu'elle
                cesar=cesar+lettre
        return cesar

    def dechiffrement(self, texte, cle, alphabet):
        """Fonction éffectuant un déchiffrement César"""
        if cle < 0:
            cle=cle*-1
        cesar=""
        for lettre in texte:
            position=alphabet.find(lettre) # position avant cryptage cesar, ex : alphabet.find('z') = 25
            # Si le lettre n'est pas dans l'alphabet on la laisse telle qu'elle
            if position != -1:
                position=position-cle
                while position >= len(alphabet):
                    position=position-len(alphabet)
                cesar=cesar+alphabet[position]
            elif alphabet.upper().find(lettre) != -1: # Si la lettre est une majuscule
                position=alphabet.find(lettre.lower())
                position=position-cle
                while position >= len(alphabet):
                    position=position-len(alphabet)
                cesar=cesar+alphabet[position].upper()
            else:
                cesar=cesar+lettre

return cesar

    def decryptage(self, texte, alphabet):
        """Fonction effectuant une cryptanalyse d'un texte chiffré avec César"""
        # Dans l'ordre : Fréquences d’apparitions des lettres en Français
        francais=['e','s','a','n','t','i','r','u','l','o','d','c','p','m','q','v','g','f','b','h','x','y','j','z','k','w']

        frequence=[]
        for lettre in texte:
            # Fréquence d'apparition des lettres dans le texte
            # avec conversion d'un des chiffre en chiffre a virgule (float) pour avoir un résultat de division a virgule :)
            frequence.append(texte.count(lettre)/float(len(texte))*100)

        # On récupère "la position" de la lettre qui revient le plus dans la liste frequence
        indice_tallest=0
        for x in range(0,len(frequence)):
            # Si c'est un caractère qui n'est pas dans l'alphabet ça compte pas ;)
            if alphabet.find(texte[x]) != -1:
                if (frequence[x]>frequence[indice_tallest]):
                    indice_tallest=x
        entete="\nLe caractère qui revient le plus dans notre texte\net qui est compris dans l'alphabet est \""+texte[indice_tallest]+"\""
        entete+="\n\nFréquance d'apparition : "+str(frequence[indice_tallest])+"%\n"

        compteur=0
        for x in francais:
            compteur=compteur+1
            # Recherche de la clé
            cle=len((alphabet.split(texte[indice_tallest])[1]+alphabet.split(texte[indice_tallest])[0]).split(x)[0])+1
            # Traitement
            cesar=""
            for lettre in texte:
                position=alphabet.find(lettre) # Position avant chiffrement cesar, ex : alphabet.find('z') = 25
                # Si la lettre n'est pas dans l'alphabet on la laisse telle qu'elle
                if position != -1:
                    position=position-cle
                    while position >= len(alphabet):
                        position=position-len(alphabet)
                    cesar=cesar+alphabet[position]
                elif alphabet.upper().find(lettre) != -1: # Si la lettre est une majuscule
                    position=alphabet.find(lettre.lower())
                    position=position-cle
                    while position >= len(alphabet):
                        position=position-len(alphabet)
                    cesar=cesar+alphabet[position].upper()
                else:
                    cesar=cesar+lettre
            if len(cesar) > 20:
                extrait=cesar[0:20]+"[...]"
            else:
                extrait=cesar
            dialog=entete+"\nClé testée : "+str(cle)+"\n\nRésultat : \""+extrait+"\""

            dialog+="\n\nLe résultat vous satisfait-il ?"
            if self.yesnoDialog(dialog):
                return cesar
            elif compteur == len(alphabet):
                return "Vous avez essayé toutes les possibilités êtes-vous sûr d'avoir fait attention ?\nL'alphabet utilisé n'est peut-être pas bon ..."

    def checkCesar(self, widget):
        """Permet d'appeler la fonction coorespondant aux choix que l'utilisateur a exprimé via l'interface graphique.
        À savoir le chiffrement, le déchiffrement ou le décryptage via cryptanalyse (ici analyse de récurances des lettres)"""
        # Buffer et texte d'entrée
        txtbuf_entree = self.textview_entree_cesar.get_buffer()
        txt_entree = txtbuf_entree.get_text(txtbuf_entree.get_start_iter(),txtbuf_entree.get_end_iter())

        # Buffer, début et fin de buffer de sortie
        txtbuf_sortie = self.textview_sortie_cesar.get_buffer()
        start_iter_sortie = txtbuf_sortie.get_start_iter()
        end_iter_sortie = txtbuf_sortie.get_end_iter()

        # Suppression du texte de sortie
        txtbuf_sortie.delete(start_iter_sortie, end_iter_sortie)

        # Chiffrement
        if self.btn_radio_ch.get_active():
            txtbuf_sortie.insert(start_iter_sortie, self.chiffrement(txt_entree,int(self.entry_rot_cesar.get_text()),self.entry_alphabet_cesar.get_text()))

        # Déchiffrement (clé connue)
        elif self.btn_radio_dech_co.get_active():
            txtbuf_sortie.insert(start_iter_sortie, self.dechiffrement(txt_entree,int(self.entry_rot_cesar.get_text()),self.entry_alphabet_cesar.get_text()))

        # Déchiffrement (clé inconnue)
        elif self.btn_radio_dech_inco.get_active():
            txtbuf_sortie.insert(start_iter_sortie, self.decryptage(txt_entree,self.entry_alphabet_cesar.get_text()))

# SUBSTITUTION MONO-ALPHABETIQUE

    def checkSubstMonoAlpha(self, widget):
        # Buffer et texte d'entrée
        txtbuf_entree_substma = self.textview_entree_substma.get_buffer()
        txt_entree_substma = txtbuf_entree_substma.get_text(txtbuf_entree_substma.get_start_iter(),txtbuf_entree_substma.get_end_iter())

        # Buffer, début et fin de buffer de sortie
        txtbuf_sortie_substma = self.textview_sortie_substma.get_buffer()
        start_iter_sortie_substma = txtbuf_sortie_substma.get_start_iter()
        end_iter_sortie_substma = txtbuf_sortie_substma.get_end_iter()

        # Suppression du texte de sortie
        txtbuf_sortie_substma.delete(start_iter_sortie_substma, end_iter_sortie_substma)

        text_origine = txt_entree_substma
        texte_substitue = ""

        alphabet_origine = self.entry_alphabet1_substma.get_text()
        alphabet_substitution =    self.entry_alphabet2_substma.get_text()

        if len(alphabet_origine) != len(alphabet_substitution):
            self.warnDialog("L'alphabet 1 et l'alphabet 2 doivent contenir un même nombre de caractères !")
        else:
            for lettre in text_origine:
                if lettre not in alphabet_origine: texte_substitue += lettre
                else: texte_substitue += alphabet_substitution[alphabet_origine.find(lettre)]

            # Écrire en sortie
            txtbuf_sortie_substma.insert(start_iter_sortie_substma, texte_substitue)

# HASH

    def calcHash(self, widget):
        """Permet de calculer le hash coorespondant aux choix que l'utilisateur a exprimé via l'interface graphique
        (Utilise la librairie hashlib)"""
        # Texte
        if self.btn_radio_text_hash.get_active():
            # Buffer et texte d'entrée
            txtbuf_entree_hash = self.textview_entree_hash.get_buffer()
            txt_entree_hash = txtbuf_entree_hash.get_text(txtbuf_entree_hash.get_start_iter(),txtbuf_entree_hash.get_end_iter())

            if txt_entree_hash != "":
                # md5
                if self.btn_radio_md5.get_active():
                    self.entry_result_hash.set_text(hashlib.md5(txt_entree_hash).hexdigest())

                # sha1
                elif self.btn_radio_sha1.get_active():
                    self.entry_result_hash.set_text(hashlib.sha1(txt_entree_hash).hexdigest())

                # sha224
                elif self.btn_radio_sha224.get_active():
                    self.entry_result_hash.set_text(hashlib.sha224(txt_entree_hash).hexdigest())

                # sha256
                elif self.btn_radio_sha256.get_active():
                    self.entry_result_hash.set_text(hashlib.sha256(txt_entree_hash).hexdigest())

                # sha384
                elif self.btn_radio_sha384.get_active():
                    self.entry_result_hash.set_text(hashlib.sha384(txt_entree_hash).hexdigest())

                # sha512
                elif self.btn_radio_sha512.get_active():
                    self.entry_result_hash.set_text(hashlib.sha512(txt_entree_hash).hexdigest())
            else:
                self.warnDialog("Veuillez saisir du texte !")

        # Fichier
        elif self.btn_radio_fichier_hash.get_active():
            path = self.entry_fichier_hash.get_text()
            if path != "":
                #self.entry_result_hash.set_text(self.sumfile(path))
                self.mkThreadSum()
            else:
                self.warnDialog("Veuillez séléctionner un fichier !")

    def sumfile(self):
        """Permet le calcul du hash (md5, sha1, sha224, sha256, sha384 ou sha512) d'un fichier"""
        self.cleanHash()

        # Désactivation des éléments graphiques pour bloquer les saisies utilisateur pendant le calcul.
        self.btn_radio_md5.set_sensitive(False)
        self.btn_radio_sha1.set_sensitive(False)
        self.btn_radio_sha224.set_sensitive(False)
        self.btn_radio_sha256.set_sensitive(False)
        self.btn_radio_sha384.set_sensitive(False)
        self.btn_radio_sha512.set_sensitive(False)
        self.btn_radio_text_hash.set_sensitive(False)
        self.btn_radio_fichier_hash.set_sensitive(False)
        self.entry_fichier_hash.set_sensitive(False)
        self.btn_fichier_hash.set_sensitive(False)

        # Afficher l'animation de traitement (image .gif) et masquer le bouton "Calculer"
        self.btn_calc_hash.hide()
        self.img_calc_hash.show()

        fileObj = open(self.entry_fichier_hash.get_text(), 'rb')

        # md5
        if self.btn_radio_md5.get_active():
            m = hashlib.md5()
        # sha1
        elif self.btn_radio_sha1.get_active():
            m = hashlib.sha1()
        # sha224
        elif self.btn_radio_sha224.get_active():
            m = hashlib.sha224()
        # sha256
        elif self.btn_radio_sha256.get_active():
            m = hashlib.sha256()
        # sha384
        elif self.btn_radio_sha384.get_active():
            m = hashlib.sha384()
        # sha512
        elif self.btn_radio_sha512.get_active():
            m = hashlib.sha512()

        while True:
            d = fileObj.read(8096)
            if not d:
                break
            m.update(d)

        # Masquer l'animation de traitement (image .gif) et réafficher le bouton "Calculer"
        self.img_calc_hash.hide()
        self.btn_calc_hash.show()

        # Réactivation des éléments graphiques de saisie utilisateur
        self.btn_radio_md5.set_sensitive(True)
        self.btn_radio_sha1.set_sensitive(True)
        self.btn_radio_sha224.set_sensitive(True)
        self.btn_radio_sha256.set_sensitive(True)
        self.btn_radio_sha384.set_sensitive(True)
        self.btn_radio_sha512.set_sensitive(True)
        self.btn_radio_text_hash.set_sensitive(True)
        self.btn_radio_fichier_hash.set_sensitive(True)
        self.entry_fichier_hash.set_sensitive(True)
        self.btn_fichier_hash.set_sensitive(True)

        # Affichage du résultat
        self.entry_result_hash.set_text(m.hexdigest())

    def cleanHash(self, widget=None, option=None):
        """Vide le champ résultat et gère la transition d'interface entre le calcul du hash d'un fichier et celui d'un texte"""
        self.entry_result_hash.set_text("")
        if option:
            if self.btn_radio_text_hash.get_active():
                # Désactivation de partie fichier, activation de partie texte
                self.entry_fichier_hash.set_sensitive(False)
                self.btn_fichier_hash.set_sensitive(False)
                self.textview_entree_hash.set_sensitive(True)
            else:
                # Désactivation de partie texte, activation de partie fichier
                self.textview_entree_hash.set_sensitive(False)
                self.entry_fichier_hash.set_sensitive(True)
                self.btn_fichier_hash.set_sensitive(True)

# MD5

    def check_kalkulators(self, hash):
        """Parsage du site kalkulators"""

        res_check = ""

        self.progressbarMd5.set_text("Recherche en cours (cracker.kalkulators.org) ...")

        cnx = httplib2.Http()
        try:
            ret = self.requete_http(cnx, "GET", "http://cracker.kalkulators.org/API/md5/raw/"+hash+"/")
            print ret
            if ret != "":
                res_check += hash + " : " + ret + "\n"
                self.pwn_hash=1
            else:
                res_check += hash+" : pas de résultat (cracker.kalkulators.org)\n"
        except:
            res_check += "cracker.kalkulators.org : le serveur ne répond pas\n"
            self.kalkulators_down = 1

        return res_check

    def check_gromweb(self, hash):
        """Parsage du site md5.gromweb.com"""

        res_check = ""

        self.progressbarMd5.set_text("Recherche en cours (md5.gromweb.com) ...")

        cnx = httplib2.Http()
        try:
            ret = self.requete_http(cnx, "GET", "http://md5.gromweb.com/query/"+hash)
            if ret != "":
                res_check += hash + " : " + ret + "\n"
                self.pwn_hash=1
            else:
                res_check += hash+" : pas de résultat (md5.gromweb.com)\n"
        except:
            res_check += "md5.gromweb.com : le serveur ne répond pas\n"
            self.gromweb_down = 1

        return res_check

    def check_onlinehashcrack(self, hash):
        """Parsage du site onlinehashcrack"""

        res_check = ""

        self.progressbarMd5.set_text("Recherche en cours (onlinehashcrack.com) ...")

        cnx = httplib2.Http()
        try:
            ret = self.requete_http(cnx, "POST", "http://www.onlinehashcrack.com/free-hash-reverse.php", {"hashToSearch":hash,"searchHash":"Search"})
            if "Your hash is not (yet ?) in our databases." not in ret:
                res_check += hash + " : " + re.compile("Plain text : <b style=\"letter-spacing:1\.2px\">(.*?)</b><br />").search(ret).group(1) + "\n"
                self.pwn_hash=1
            else:
                res_check += hash+" : pas de résultat (onlinehashcrack.com)\n"
        except:
            res_check += "onlinehashcrack.com : le serveur ne répond pas\n"
            self.onlinehashcrack_down = 1

        return res_check

    def check_c0llision(self, hash):
        """Parsage du site c0llision"""

        res_check = ""

        self.progressbarMd5.set_text("Recherche en cours (c0llision.net) ...")

        cnx = httplib2.Http()
        try:
            ret = self.requete_http(cnx, "GET", "http://api.dev.c0llision.net/crack/md5/"+hash)
            if "<cracked>false</cracked>" not in ret:
                res_check += hash + " : " + re.compile("<raw>(.*?)</raw>").search(ret).group(1) + "\n"
                self.pwn_hash=1
            else:
                res_check += hash+" : pas de résultat (c0llision.net)\n"
        except:
            res_check += "c0llision.net : le serveur ne répond pas\n"
            self.onlinehashcrack_down = 1

        return res_check

    def check_xanadrel(self, hash):
        """Parsage du site xanadrel"""

        res_check = ""

        self.progressbarMd5.set_text("Recherche en cours (xanadrel.99k.org) ...")

        cnx = httplib2.Http()
        try:
            ret = self.requete_http(cnx, "GET", "http://xanadrel.99k.org/hashes/api.php?hash="+hash)
            if "<found>yes</found>" in ret:
                res_check += hash + " : " + re.compile("<plain>(.*?)</plain>").search(ret).group(1) + "\n"
                self.pwn_hash=1
            else:
                res_check += hash+" : pas de résultat (xanadrel.99k.org)\n"
        except:
            res_check += "xanadrel.99k.org : le serveur ne répond pas\n"
            self.xanadrel_down = 1

        return res_check

    def check_md5lookup(self, hash):
        """Parsage du site md5-lookup"""

        res_check = ""

        self.progressbarMd5.set_text("Recherche en cours (md5-lookup.com) ...")

        cnx = httplib2.Http()
        try:
            ret = self.requete_http(cnx, "GET", "http://www.md5-lookup.com/index.php?q="+hash)
            if "No results found!" not in ret:
                res_check += hash + " : " + re.compile("<td width=\"250\">(.*?)</td>").search(ret).group(1) + "\n"
                self.pwn_hash=1
            else:
                res_check += hash+" : pas de résultat (md5-lookup.com)\n"
        except:
            res_check += "md5-lookup.com : le serveur ne répond pas\n"
            self.xanadrel_down = 1

        return res_check

    def check_md5rednoize(self, hash):
        """Parsage du site md5 rednoize"""

        res_check = ""

        self.progressbarMd5.set_text("Recherche en cours (md5.rednoize.com) ...")

        cnx = httplib2.Http()
        try:
            ret = self.requete_http(cnx, "GET", "http://md5.rednoize.com/?s=md5&q="+hash)
            if "result\" style=\"display:none;" not in ret:
                res_check += hash + " : " + re.compile("<div id=\"result\" >(.*?)</div>").search(ret).group(1) + "\n"
                self.pwn_hash=1
            else:
                res_check += hash+" : pas de résultat (md5.rednoize.com)\n"
        except:
            res_check += "md5.rednoize.com : le serveur ne répond pas\n"
            self.md5rednoize_down = 1

        return res_check

    def check_toolsbenramsey(self, hash):
        """Parsage du site tools benramsey"""

        res_check = ""

        self.progressbarMd5.set_text("Recherche en cours (tools.benramsey.com) ...")

        cnx = httplib2.Http()
        try:
            ret = self.requete_http(cnx, "GET", "http://tools.benramsey.com/md5/md5.php?hash="+hash)
            if "error" not in ret:
                res_check += hash + " : " + re.compile("<string><\!\[CDATA\[(.*?)\]\]></string>").search(ret).group(1) + "\n"
                self.pwn_hash=1
            else:
                res_check += hash+" : pas de résultat (tools.benramsey.com)\n"
        except:
            res_check += "tools.benramsey.com : le serveur ne répond pas\n"
            self.toolsbenramsey_down = 1

        return res_check

    def checkmd5_online(self):
        """Module de recheche de hash md5 en ligne"""
        # Au cas où des sites seraient down (ou qu'il n'y ai pas d'accès internet)
        #self.kalkulators_down = 0
        self.gromweb_down = 0
        self.onlinehashcrack_down = 0
        self.c0llision_down = 0
        self.xanadrel_down = 0
        self.md5lookup_down = 0
        self.md5rednoize_down = 0
        self.toolsbenramsey_down = 0

        # Désactivation du boutton de validation pour éviter de lancer plusieur recherche simultanement
        self.btn_checkmd5.set_sensitive(False)

        # Activer l'animation de la progressbar et changer son label
        self.enCoursMd5=1
        self.progressbarMd5.set_text("Recherche en cours ...")
        t2 = thread.start_new_thread(self.runProgressbarMd5, ())

        # Connaitre l'heure de début pour le calcul du temps pris
        start_time_md5 = time()

        # Buffer et texte d'entrée
        txtbuf_entree_md5 = self.textview_entree_md5.get_buffer()
        txt_entree_md5 = txtbuf_entree_md5.get_text(txtbuf_entree_md5.get_start_iter(),txtbuf_entree_md5.get_end_iter())

        # Buffer, début et fin de buffer de sortie
        txtbuf_sortie_md5 = self.textview_sortie_md5.get_buffer()
        start_iter_sortie_md5 = txtbuf_sortie_md5.get_start_iter()
        end_iter_sortie_md5 = txtbuf_sortie_md5.get_end_iter()

        # Suppression du texte de sortie
        txtbuf_sortie_md5.delete(start_iter_sortie_md5, end_iter_sortie_md5)

        ls_hash = re.compile("^[\w]{32}", re.MULTILINE).findall(txt_entree_md5)

        for hash in ls_hash:
            self.pwn_hash=0

            #if not self.kalkulators_down:
            #if self.checkbtn_kalkulators.get_active():
            #txtbuf_sortie_md5.insert(start_iter_sortie_md5, self.check_kalkulators(hash))
            if not self.gromweb_down:
                if self.pwn_hash == 0:
                    if self.checkbtn_gromweb.get_active():
                        txtbuf_sortie_md5.insert(start_iter_sortie_md5, self.check_gromweb(hash))
            if not self.onlinehashcrack_down:
                if self.pwn_hash == 0:
                    if self.checkbtn_onlinehashcrack.get_active():
                        txtbuf_sortie_md5.insert(start_iter_sortie_md5, self.check_onlinehashcrack(hash))
            if not self.c0llision_down:
                if self.pwn_hash == 0:
                    if self.checkbtn_c0llision.get_active():
                        txtbuf_sortie_md5.insert(start_iter_sortie_md5, self.check_c0llision(hash))
            if not self.xanadrel_down:
                if self.pwn_hash == 0:
                    if self.checkbtn_xanadrel.get_active():
                        txtbuf_sortie_md5.insert(start_iter_sortie_md5, self.check_xanadrel(hash))
            if not self.md5lookup_down:
                if self.pwn_hash == 0:
                    if self.checkbtn_md5lookup.get_active():
                        txtbuf_sortie_md5.insert(start_iter_sortie_md5, self.check_md5lookup(hash))
            if not self.md5rednoize_down:
                if self.pwn_hash == 0:
                    if self.checkbtn_md5rednoize.get_active():
                        txtbuf_sortie_md5.insert(start_iter_sortie_md5, self.check_md5rednoize(hash))
            if not self.toolsbenramsey_down:
                if self.pwn_hash == 0:
                    if self.checkbtn_toolsbenramsey.get_active():
                        txtbuf_sortie_md5.insert(start_iter_sortie_md5, self.check_toolsbenramsey(hash))

        # Traitement terminé arrêt de l'animation de la progressbar et changement de son label
        self.enCoursMd5=0
        self.progressbarMd5.set_fraction(1.0)
        self.duree_scan_md5 = time()-start_time_md5
        self.progressbarMd5.set_text("Recherche terminée (effectuée en "+strftime('%H:%M:%S', gmtime(int(self.duree_scan_md5)))+")")

        # Affichage d'une notification
        if pynotify.init("Free-knowledge Toolbox"):
            n = pynotify.Notification("Free-knowledge Toolbox", "MD5 - Recherche terminée", "%s/images/icone.png" % FKTB_PATH)
            if not n.show(): print "échec de notification ..."
        else:
            if "not found" in getoutput('notify-send -i %s/images/icone.png -t 0 "Free-knowledge Toolbox" "MD5 - Recherche terminée"' % FKTB_PATH):
                print "notify-send n'est pas installé ..."

        # Réactivation du boutton de validation
        self.btn_checkmd5.set_sensitive(True)

# REGEX WEB

    def regex_http(self, widget):
        page_web = self.entry_url_wregex.get_text()
        if page_web != "":
            if page_web[0:7] != "http://" and page_web[0:8] != "https://" :
                page_web="http://"+page_web

            cnx = httplib2.Http()
            try: ret = self.requete_http(cnx, "GET", page_web)
            except: ret = "Impossible de trouver le serveur à l'adresse "+page_web

            # Buffer, début et fin de buffer pour le code source
            txtbuf_source_wregex = self.textview_source_wregex.get_buffer()
            start_iter_source_wregex = txtbuf_source_wregex.get_start_iter()
            end_iter_source_wregex = txtbuf_source_wregex.get_end_iter()

            # Suppression du code source affiché
            txtbuf_source_wregex.delete(start_iter_source_wregex, end_iter_source_wregex)
            txtbuf_source_wregex.insert(start_iter_source_wregex, ret)

            # Buffer, début et fin de buffer de sortie
            txtbuf_result_wregex = self.textview_result_wregex.get_buffer()
            start_iter_result_wregex = txtbuf_result_wregex.get_start_iter()
            end_iter_result_wregex = txtbuf_result_wregex.get_end_iter()

            # Suppression du texte de sortie
            txtbuf_result_wregex.delete(start_iter_result_wregex, end_iter_result_wregex)

            # Recupération des résultats du parsage
            regex = self.entry_reg_wregex.get_text()
            if regex != "":
                try: res = re.compile(regex, re.MULTILINE).findall(ret)
                except:
                    self.warnDialog("Erreur dans l'expression rationnelle !")
                    self.label_result_wregex.set_text("Résultat : (erreur)")
                    self.label_result_wregex.hide()
                    self.label_result_wregex.show()
                else:
                    txtbuf_result_wregex.insert(start_iter_result_wregex, "\n".join(res))    # Affichage du résultat
                    self.label_result_wregex.set_text("Résultat : ("+str(len(res))+")")    # Affichage du nombre de résultat
                    self.label_result_wregex.hide()
                    self.label_result_wregex.show()
            else:
                ret = re.sub('[\s]+$', '', re.sub('^[\s]+', '', ret))                # Enlever les caractères d'espacement en début et fin de chaîne
                txtbuf_result_wregex.insert(start_iter_result_wregex, ret)            # Affichage du résultat
                self.label_result_wregex.set_text("Résultat : ("+str(len(ret.split("\n")))+")")    # Affichage du nombre de résultat
                self.label_result_wregex.hide()
                self.label_result_wregex.show()

# MAIL

    def envoyer_mail(self,date_envoi_mail):
        # Récupération de l'adresse mail de l'émetteur
        addresse_mail_source = self.entry_mail_from.get_text()

        # Récupération de l'adresse mail du destinataire
        addresse_mail_du_destinataire = self.entry_mail_to.get_text()

        # Récupération du sujet du mail
        sujet_du_mail = self.entry_mail_sujet.get_text()

        # Récupération du corps du mail
        txtbuf_mail_corps = self.textview_mail_corps.get_buffer()
        corps_du_mail = txtbuf_mail_corps.get_text(txtbuf_mail_corps.get_start_iter(),txtbuf_mail_corps.get_end_iter())

        # Récupération du chemin vers la pièce jointe
        fichier_joint = self.entry_mail_piece_j.get_text()

        # Récupération du serveur SMTP
        serveur_smtp = self.entry_mail_smtp.get_text()

        # Récupération du nombre de mail à envoyer
        nombre_envoi = self.entry_mail_nb_env.get_text()

        # Désactivation du bouton d'envoi
        self.btn_env_mail.set_sensitive(False)

        # Activer l'animation de la progressbar et changer son label
        self.enCoursMail=1
        self.progressbarMail.set_text("Envoi en cours ...")
        t2 = thread.start_new_thread(self.runProgressbarMail, ())

        # Connaitre l'heure de début pour le calcul du temps pris
        start_time_mail = time()

        i=1
        erreur=0
        while int(i) <= int(nombre_envoi) and not erreur:
            msg = MIMEMultipart()
            msg['From']=addresse_mail_source
            msg['To']=addresse_mail_du_destinataire
            msg['Date']=date_envoi_mail # date
            msg['Subject']=sujet_du_mail
            msg.attach(MIMEText(corps_du_mail))
            if fichier_joint != '': # si on veux envoyer un fichier
                part = MIMEBase('applciation', "octet-stream")
                part.set_payload(open(fichier_joint).read())
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"'%os.path.basename(fichier_joint))
                msg.attach(part)
            try:
                server=smtplib.SMTP(serveur_smtp)
                server.set_debuglevel(0)
                server.sendmail(addresse_mail_source, addresse_mail_du_destinataire, msg.as_string())
                server.quit()
            except:
                # Traitement terminé arrêt de l'animation de la progressbar et changement de son label
                self.enCoursMail=0
                self.progressbarMail.set_fraction(1.0)
                self.progressbarMail.set_text("Erreur d'envoi !")

                # Affichage d'une notification
                if pynotify.init("Free-knowledge Toolbox"):
                    n = pynotify.Notification("Free-knowledge Toolbox", "Mail - Erreur d\'envoi", "%s/images/icone.png" % FKTB_PATH)
                    if not n.show(): print "échec de notification ..."
                else:
                    if "not found" in getoutput('notify-send -i %s/images/icone.png -t 0 "Free-knowledge Toolbox" "Mail - Erreur d\'envoi"' % FKTB_PATH):
                        print "notify-send n'est pas installé ..."

                # Réactivation du boutton de validation
                self.btn_env_mail.set_sensitive(True)
                erreur=1
            else:
                self.progressbarMail.set_text("Mail "+str(i)+"/"+nombre_envoi+" envoyé")

                if str(i) == nombre_envoi:
                    # Affichage d'une notification
                    if pynotify.init("Free-knowledge Toolbox"):
                        n = pynotify.Notification("Free-knowledge Toolbox", "Mail - Envoi terminé", "%s/images/icone.png" % FKTB_PATH)
                        if not n.show(): print "échec de notification ..."
                    else:
                        if "not found" in getoutput('notify-send -i %s/images/icone.png -t 0 "Free-knowledge Toolbox" "Mail - Envoi terminé"' % FKTB_PATH):
                            print "notify-send n'est pas installé ..."
                i=i+1

        if not erreur:
            # Traitement terminé arrêt de l'animation de la progressbar et changement de son label
            self.enCoursMail=0
            self.progressbarMail.set_fraction(1.0)
            self.duree_env_mail = time()-start_time_mail
            self.progressbarMail.set_text("Envoi terminé (effectué en "+strftime('%H:%M:%S', gmtime(int(self.duree_env_mail)))+")")

        # Réactivation du boutton de validation
        self.btn_env_mail.set_sensitive(True)

# STRINGS

    def stringsFichier(self, parent):
        #self.entry_strings.set_text(self.dialogueOuvrirStrings())
        reponse = self.entry_strings.get_text()
        if reponse != "":
            # Buffer, début et fin de buffer de sortie
            txtbuf_result_strings = self.textview_result_strings.get_buffer()
            start_iter_result_strings = txtbuf_result_strings.get_start_iter()
            end_iter_result_strings = txtbuf_result_strings.get_end_iter()

            # Suppression du texte de sortie
            txtbuf_result_strings.delete(start_iter_result_strings, end_iter_result_strings)

            # Recupération des résultats du parsage
            regex = self.entry_reg_strings.get_text()
            strings = getoutput("strings \""+reponse+"\"")
            if regex != "":
                try: res = re.compile(regex, re.MULTILINE).findall(strings)
                except:
                    self.warnDialog("Erreur dans l'expression rationnelle !")
                    self.label_result_strings.set_text("Résultat : (erreur)")
                    self.label_result_strings.hide()
                    self.label_result_strings.show()
                else:
                    txtbuf_result_strings.insert(start_iter_result_strings, "\n".join(res))    # Affichage du résultat
                    self.label_result_strings.set_text("Résultat : ("+str(len(res))+")")    # Affichage du nombre de résultat
                    self.label_result_strings.hide()
                    self.label_result_strings.show()
            else:
                txtbuf_result_strings.insert(start_iter_result_strings, strings)            # Affichage du résultat
                self.label_result_strings.set_text("Résultat : ("+str(len(strings.split("\n")))+")")    # Affichage du nombre de résultat
                self.label_result_strings.hide()
                self.label_result_strings.show()
        else:
            self.dialogueOuvrirStrings("")

# ASM

    def asm2human(self, parent):
        app_path = self.entry_bin_asm.get_text().replace(' ','\ ')
        desass = self.entry_desass_asm.get_text()

        if desass != "":
            if app_path != "":
                conversion=""
                lst_erreur=[] # Pour les instructions manquantes

                # Dictionnaire d'équivalence ASM - "Langage Humain"
                dico_asm = {#'add' : 'ADD - ...',
                            #'addl' : 'ADDL - ...',
                            #'cmpl' : 'CMPL - ...',
                            #'leave' : 'Permet de libérer une zone de mémoire',
                            #'movl' : 'MOVL - ...',
                            #'movzbl' : 'MOVZBL - ...',
                            'pushl' : 'PUSHL {a} : Sauvegarde {a} dans la pile.',
                            'sub' : 'SUB {a} {b} : Soustrait {b} de {a} et entrepose le résultat dans {a}.',
                            'pop' : 'POP {a} : Désempile du sommet de la pile une valeur et la met dans {a}.',
                            'add' : 'ADD {a} {b} : Ajout de {b} à {a}',
                            'and' : 'Applique un "et" à {destination} par {masque}.',
                            'call' : 'Appelle une procédure qui est à l\'adresse {adresse}.',
                            'cmp' : 'Compare les deux variables {a} et {b}.',
                            'je' : 'Va ("J" = Jump : Sauter) à l\'adresse {offset} si {a} est égale à {b}.',
                            'jmp' : 'JMP {offset} : Va à l\'adresse {offset}.',
                            'jne' : 'Va à l\'adresse {offset} si {a} est différent de {b}.',
                            'jle' : 'Va à l\'adresse {offset} si {a} est plus petit ou égale à {b}.',
                            'jg' : 'Va à l\'adresse {offset} si {a} est supérieur à {b}',
                            'jge' : 'Va à l\'adresse {offset} si {a} est supérieur ou égale à {b}',
                            'lea' : 'LEA {destination},{source} : Ecrit l\'adresse de {source} dans {destination}. Equivaut à "MOV {destination}, OFFSET {source}".',
                            'mov' : 'MOV {dst},{src} : Copie la valeur {src} dans {dst}.',
                            'push' : 'PUSH {valeur} : Met une [valeur] dans la pile.',
                            'ret' : 'RET {valeur} : Quitte la procédure en cours. Si des paramètres ont été envoyés au CALL, [xxxx] est le nombre d\'octets envoyés qui sont à sortir de la pile.',
                            'test' : 'TEST {source},{masque} : Teste si les bits {masque} de {source} sont posés ou non, et modifie ZF en conséquence (ZF posé si les bits de {source} sont posés, sinon ZF=0), ce qui sera exploitable avec "JZ" ou "JNZ" par la suite. L\'instruction permet de tester un bit particulier de {source}.\nEn particulier : TEST {a},{a} = Teste si la variable {a} est à zéro (pose ou non le drapeau ZF).'}


                gdb_commands = "disassemble "+desass+"\nq\n"

                # Écriture du fichier contenant les commandes
                output = open("gdb_commands",'wb')
                output.write(gdb_commands)
                output.close()

                # Bidouillage pour récupérer un "disassemble quelque-chose" sur l'application passée en paramètre
                result=re.compile("^[ ]*(0x[a-f0-9]*) (<\+[0-9]*>):\t([a-z]*)[ ]*(.*$)", re.MULTILINE).findall(getoutput('echo|gdb '+app_path+' -q -x gdb_commands && rm gdb_commands'))

                if len(result) != 0:
                    for ligne in result:
                        instruction=ligne[2]
                        try: self.liststore_asm.append((ligne[0], ligne[1], ligne[2]+" "+ligne[3], instruction.replace(instruction, dico_asm[instruction])))
                        except KeyError:
                            self.liststore_asm.append((ligne[0], ligne[1], ligne[2]+" "+ligne[3], instruction.upper()+" - Aucune information pour l'instant"))
                            lst_erreur.append("L'instruction \""+instruction+"\" n'est pas renseigné...")
                    if len(lst_erreur): self.warnDialog(("\n").join(sorted(set(lst_erreur)))+"\n\n... une petite modif du code ? xD")
                else: self.warnDialog("Aucune ligne d'ASM à \"traduire\" avec l'instruction :\n\n\tdisassemble "+desass)
            else:
                self.dialogueOuvrirBin("")
                self.asm2human("")
        else : self.warnDialog("Veuillez entrer le nom d'une fonction à désassembler")

# COUCHES RVB

    def hideMsg(self, widget=None):
        try:
            self.im = Image.open(self.entry_img_c_rgb.get_text())
        except IOError:
            # On cache la partie affichage
            self.boite_apercu_c_rgb.hide()

            self.warnDialog("Ce fichier n'est pas une image valide !")
        else:
            self.im.load()
            # On récupère les dimensions de l'image
            w,h=self.im.size
            # On éclate l'image en trois (rouge vert bleu)
            try:
                r,v,b=self.im.split()
            except ValueError:
                # On cache la partie affichage
                self.boite_apercu_c_rgb.hide()

                self.warnDialog("Les images avec transparence ne sont pas encore gérées :/")
            else:
                # On transforme l'image en liste
                if self.btn_radio_rouge_c_rgb.get_active():
                    r=list(r.getdata())
                elif self.btn_radio_vert_c_rgb.get_active():
                    v=list(v.getdata())
                elif self.btn_radio_bleu_c_rgb.get_active():
                    b=list(b.getdata())
                    # On note la longueur de la chaine et on la transforme en binaire
                long_msg=len(self.texte_c_rgb)
                long_msg_bin=bin(len(self.texte_c_rgb))[2:].rjust(8,"0")
                # On converti la chaîne en binaire
                msg_bin=''.join([bin(ord(x))[2:].rjust(8,"0") for x in self.texte_c_rgb])
                # On code la longueur de la liste dans les 8 premiers pixels rouges
                for j in range(8):
                    if self.btn_radio_rouge_c_rgb.get_active():
                        r[j]=2*int(r[j]//2)+int(long_msg_bin[j])
                    elif self.btn_radio_vert_c_rgb.get_active():
                        v[j]=2*int(v[j]//2)+int(long_msg_bin[j])
                    elif self.btn_radio_bleu_c_rgb.get_active():
                        b[j]=2*int(b[j]//2)+int(long_msg_bin[j])
                        # On code la chaine dans les pixels suivants
                for i in range(8*long_msg):
                    if self.btn_radio_rouge_c_rgb.get_active():
                        r[i+8]=2*int(r[i+8]//2)+int(msg_bin[i])
                    elif self.btn_radio_vert_c_rgb.get_active():
                        v[i+8]=2*int(v[i+8]//2)+int(msg_bin[i])
                    elif self.btn_radio_bleu_c_rgb.get_active():
                        b[i+8]=2*int(b[i+8]//2)+int(msg_bin[i])
                        # On recrée l'image rouge
                if self.btn_radio_rouge_c_rgb.get_active():
                    nr = Image.new("L",(w,h))
                    nr.putdata(r)
                    # Fusion des trois nouvelles images
                    imgnew = Image.merge('RGB',(nr,v,b))
                elif self.btn_radio_vert_c_rgb.get_active():
                    nv = Image.new("L",(w,h))
                    nv.putdata(v)
                    # Fusion des trois nouvelles images
                    imgnew = Image.merge('RGB',(r,nv,b))
                elif self.btn_radio_bleu_c_rgb.get_active():
                    nb = Image.new("L",(w,h))
                    nb.putdata(b)
                    # Fusion des trois nouvelles images
                    imgnew = Image.merge('RGB',(r,v,nb))
                imgnew.save("%s/tmp/result_stega.png" % FKTB_PATH)

                # On affiche l'image
                self.img_result = gtk.Image()
                self.img_result.set_from_file("%s/tmp/result_stega.png" % FKTB_PATH)
                self.scrolled_img_result_c_rgb.add_with_viewport(self.img_result)
                self.img_result.show()

    def readMsg(self, widget=None):
        # Buffer, début et fin de buffer du texte
        txtbuf_texte_c_rgb = self.textview_texte_c_rgb.get_buffer()
        start_iter_texte_c_rgb = txtbuf_texte_c_rgb.get_start_iter()
        end_iter_texte_c_rgb = txtbuf_texte_c_rgb.get_end_iter()

        # On vide la textview
        txtbuf_texte_c_rgb.delete(start_iter_texte_c_rgb, end_iter_texte_c_rgb)

        try:
            self.im = Image.open(self.entry_img_c_rgb.get_text())
        except IOError:
            # On cache la partie affichage
            self.boite_apercu_c_rgb.hide()

            self.warnDialog("Ce fichier n'est pas une image valide !")
        else:
            self.im.load()
            try:
                r,v,b=self.im.split()
            except ValueError:
                # On cache la partie affichage
                self.boite_apercu_c_rgb.hide()

                self.warnDialog("Les images avec transparence ne sont pas encore gérées :/")
            else:
                r=list(r.getdata())
                # Lecture de la longueur de la chaine
                p=[str(x%2) for x in r[0:8]]
                q="".join(p)
                q=int(q,2)
                # Lecture du message
                n=[str(x%2) for x in r[8:8*(q+1)]]
                m="".join(n)
                message_r=""
                for k in range(0,q):
                    l=m[8*k:8*k+8]
                    message_r=message_r+chr(int(l,2))

                v=list(v.getdata())
                # Lecture de la longueur de la chaine
                p=[str(x%2) for x in v[0:8]]
                q="".join(p)
                q=int(q,2)
                # Lecture du message
                n=[str(x%2) for x in v[8:8*(q+1)]]
                m="".join(n)
                message_v=""
                for k in range(0,q):
                    l=m[8*k:8*k+8]
                    message_v=message_v+chr(int(l,2))

                b=list(b.getdata())
                # Lecture de la longueur de la chaine
                p=[str(x%2) for x in b[0:8]]
                q="".join(p)
                q=int(q,2)
                # Lecture du message
                n=[str(x%2) for x in b[8:8*(q+1)]]
                m="".join(n)
                message_b=""
                for k in range(0,q):
                    l=m[8*k:8*k+8]
                    message_b=message_b+chr(int(l,2))

                self.result_read_stega={'r':'','v':'','b':''}

                try:
                    message_r.decode('utf-8')
                except UnicodeDecodeError:
                    # Pas de message dans la couche rouge de l'image
                    self.btn_radio_rouge_c_rgb.set_sensitive(False)
                else:
                    # Message dans la couche ou faux positif ?
                    if message_r and not '\0' in message_r:
                        self.result_read_stega['r']=message_r
                        self.btn_radio_rouge_c_rgb.set_sensitive(True)
                        self.btn_radio_rouge_c_rgb.set_active(True)
                        txtbuf_texte_c_rgb.insert(start_iter_texte_c_rgb, self.result_read_stega['r'])
                    else:
                        self.btn_radio_rouge_c_rgb.set_sensitive(False)

                try:
                    message_v.decode('utf-8')
                except UnicodeDecodeError:
                    # Pas de message dans la couche verte de l'image
                    self.btn_radio_vert_c_rgb.set_sensitive(False)
                else:
                    # Message dans la couche ou faux positif ?
                    if message_v != '' and not '\0' in message_v:
                        self.result_read_stega['v']=message_v
                        self.btn_radio_vert_c_rgb.set_sensitive(True)
                        if not self.result_read_stega['r']:
                            self.btn_radio_vert_c_rgb.set_active(True)
                            txtbuf_texte_c_rgb.insert(start_iter_texte_c_rgb, self.result_read_stega['v'])
                    else:
                        self.btn_radio_vert_c_rgb.set_sensitive(False)

                try:
                    message_b.decode('utf-8')
                except UnicodeDecodeError:
                    # Pas de message dans la couche bleue de l'image
                    self.btn_radio_bleu_c_rgb.set_sensitive(False)
                else:
                    # Message dans la couche ou faux positif ?
                    if message_b != '' and not '\0' in message_b:
                        self.result_read_stega['b']=message_b
                        self.btn_radio_bleu_c_rgb.set_sensitive(True)
                        if not self.result_read_stega['r'] and not self.result_read_stega['v']:
                            self.btn_radio_bleu_c_rgb.set_active(True)
                            txtbuf_texte_c_rgb.insert(start_iter_texte_c_rgb, self.result_read_stega['b'])
                    else:
                        self.btn_radio_bleu_c_rgb.set_sensitive(False)

                if not self.result_read_stega['r'] and not self.result_read_stega['v'] and not self.result_read_stega['b']:
                    self.cleanCouchesRVB()
                    self.infoDialog("Cette image ne contient pas de message !")
                else:
                    self.boite_texte_c_rgb.show()

                    self.label_choix_couche_rgb.show()
                    self.btn_radio_rouge_c_rgb.show()
                    self.btn_radio_vert_c_rgb.show()
                    self.btn_radio_bleu_c_rgb.show()

    def choixCouchesRVB(self, widget):
        self.cleanCouchesRVB()
        if self.btn_radio_hide_c_rgb.get_active():
            self.boite_texte_c_rgb.show()
            self.textview_texte_c_rgb.set_editable(True)

            self.label_choix_couche_rgb.set_text("Quelle couche utiliser ?")
            self.label_choix_couche_rgb.show()
            self.btn_radio_rouge_c_rgb.set_sensitive(True)
            self.btn_radio_vert_c_rgb.set_sensitive(True)
            self.btn_radio_bleu_c_rgb.set_sensitive(True)
            self.btn_radio_rouge_c_rgb.set_active(True)
            self.btn_radio_rouge_c_rgb.show()
            self.btn_radio_vert_c_rgb.show()
            self.btn_radio_bleu_c_rgb.show()
            self.label_img_orig_c_rgb.set_text("Image originale :")

        else: #elif self.btn_radio_read_c_rgb.get_active():
            self.boite_texte_c_rgb.hide()
            self.textview_texte_c_rgb.set_editable(False)

            self.label_choix_couche_rgb.set_text("Couche affichée :")
            self.label_choix_couche_rgb.hide()
            self.btn_radio_rouge_c_rgb.hide()
            self.btn_radio_vert_c_rgb.hide()
            self.btn_radio_bleu_c_rgb.hide()
            self.btn_radio_rouge_c_rgb.set_sensitive(False)
            self.btn_radio_vert_c_rgb.set_sensitive(False)
            self.btn_radio_bleu_c_rgb.set_sensitive(False)
            self.label_img_orig_c_rgb.set_text("Image contenant le message :")

    def cleanCouchesRVB(self, param=None):
        # Pour éviter de devoir retaper le texte quand on change de couche couleur
        if not param:
            # On vide le champ chemin de l'image
            self.entry_img_c_rgb.set_text("")
            # Buffer, début et fin de buffer du texte
            txtbuf_texte_c_rgb = self.textview_texte_c_rgb.get_buffer()
            start_iter_texte_c_rgb = txtbuf_texte_c_rgb.get_start_iter()
            end_iter_texte_c_rgb = txtbuf_texte_c_rgb.get_end_iter()
            # On vide la textview
            txtbuf_texte_c_rgb.delete(start_iter_texte_c_rgb, end_iter_texte_c_rgb)
            # On efface les éventuelles images
        for fils in self.scrolled_img_result_c_rgb.get_children():
            self.scrolled_img_result_c_rgb.remove(fils)
        for fils in self.scrolled_img_orig_c_rgb.get_children():
            self.scrolled_img_orig_c_rgb.remove(fils)

        # On cache la partie affichage
        self.boite_apercu_c_rgb.hide()

        if self.btn_radio_read_c_rgb.get_active():
            self.label_choix_couche_rgb.hide()
            self.btn_radio_rouge_c_rgb.hide()
            self.btn_radio_vert_c_rgb.hide()
            self.btn_radio_bleu_c_rgb.hide()

            self.boite_texte_c_rgb.hide()

    def switchColor(self, param=None,param2=None):
        if self.btn_radio_read_c_rgb.get_active() and self.textview_texte_c_rgb.get_visible():
            if param2 =='r' and self.btn_radio_rouge_c_rgb.get_active():
                # Buffer, début et fin de buffer du texte
                txtbuf_texte_c_rgb = self.textview_texte_c_rgb.get_buffer()
                start_iter_texte_c_rgb = txtbuf_texte_c_rgb.get_start_iter()
                end_iter_texte_c_rgb = txtbuf_texte_c_rgb.get_end_iter()
                # On vide la textview
                txtbuf_texte_c_rgb.delete(start_iter_texte_c_rgb, end_iter_texte_c_rgb)
                txtbuf_texte_c_rgb.insert(start_iter_texte_c_rgb, self.result_read_stega['r'])
            if param2 =='v' and self.btn_radio_vert_c_rgb.get_active():
                # Buffer, début et fin de buffer du texte
                txtbuf_texte_c_rgb = self.textview_texte_c_rgb.get_buffer()
                start_iter_texte_c_rgb = txtbuf_texte_c_rgb.get_start_iter()
                end_iter_texte_c_rgb = txtbuf_texte_c_rgb.get_end_iter()
                # On vide la textview
                txtbuf_texte_c_rgb.delete(start_iter_texte_c_rgb, end_iter_texte_c_rgb)
                txtbuf_texte_c_rgb.insert(start_iter_texte_c_rgb, self.result_read_stega['v'])
            if param2 =='b' and self.btn_radio_bleu_c_rgb.get_active():
                # Buffer, début et fin de buffer du texte
                txtbuf_texte_c_rgb = self.textview_texte_c_rgb.get_buffer()
                start_iter_texte_c_rgb = txtbuf_texte_c_rgb.get_start_iter()
                end_iter_texte_c_rgb = txtbuf_texte_c_rgb.get_end_iter()
                # On vide la textview
                txtbuf_texte_c_rgb.delete(start_iter_texte_c_rgb, end_iter_texte_c_rgb)
                txtbuf_texte_c_rgb.insert(start_iter_texte_c_rgb, self.result_read_stega['b'])

# NOT

    def opNot(self, file_path):
        self.btn_img_op_not.set_sensitive(False)

        self.label_in_file_op_not.set_text("Fichier d'entrée : ("+getoutput('file -b "'+file_path+'"')+")")
        self.entry_in_file_op_not.set_text(file_path)
        self.label_out_file_op_not.set_text("Fichier en sortie :")
        self.progressbarOpNot.set_fraction(0)

        data=''
        with open(file_path, "rb") as f:
            file_in=f.read()
            file_in_len=len(file_in)

            o=0
            while o < file_in_len:
                octet=''
                for i in ['0'*(8-len(i))+i for i in [bin(ord(i)).replace('0b','') for i in file_in[o]]][0]:
                    octet+=str(int(not(int(i))))
                data+=chr(int(octet,2))
                o+=1

                gtk.gdk.threads_enter()
                # Animation de la progressbar et changement de son label
                self.progressbarOpNot.set_fraction(1.0*o/file_in_len)
                self.progressbarOpNot.set_text(str(100*o/file_in_len)+'%')
                gtk.gdk.threads_leave()

        # Écriture du binaire dans le fichier binaire_zenk_dev2
        output = open("%s/tmp/result_opnot" % FKTB_PATH,'wb')
        output.write(data)
        output.close()

        self.label_out_file_op_not.set_text("Fichier en sortie : ("+getoutput('file -b %s/tmp/result_opnot' % FKTB_PATH)+")")

        self.btn_img_op_not.set_sensitive(True)
        self.btn_save_out_op_not.set_sensitive(True)

        gtk.gdk.threads_leave() # Arret du thread

    def saveOutOpNot(self, parent):
        dialogue = gtk.FileChooserDialog("Enregister le résultat",None,gtk.FILE_CHOOSER_ACTION_SAVE,
                                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,    # bouton annuler
                                          gtk.STOCK_SAVE, gtk.RESPONSE_OK))    # bouton enregistrer
        dialogue.set_default_response(gtk.RESPONSE_OK)
        dialogue.set_current_name('Resultat_opnot')

        filtre = gtk.FileFilter()
        filtre.set_name("All files")
        filtre.add_pattern("*")
        dialogue.add_filter(filtre)

        reponse = dialogue.run()
        if reponse == gtk.RESPONSE_OK:
            sortie=dialogue.get_filename()
        else:
            sortie=0
        dialogue.destroy()
        if sortie: os.system("cp \"%s/tmp/result_opnot\" \"" % FKTB_PATH + sortie + "\"")

# XOR

    def xor(self, widget):
        # Buffer et texte d'entrée
        txtbuf_entree_xor = self.textview_entree_xor.get_buffer()
        txt_entree_xor = txtbuf_entree_xor.get_text(txtbuf_entree_xor.get_start_iter(),txtbuf_entree_xor.get_end_iter())
        # Buffer, début et fin de buffer de sortie
        txtbuf_sortie_xor = self.textview_sortie_xor.get_buffer()
        start_iter_sortie_xor = txtbuf_sortie_xor.get_start_iter()
        end_iter_sortie_xor = txtbuf_sortie_xor.get_end_iter()

        # Suppression du texte de sortie
        txtbuf_sortie_xor.delete(start_iter_sortie_xor, end_iter_sortie_xor)

        c = 0
        data = ''
        key=self.entry_key_xor.get_text()

        # 0 ascii
        # 1 décimal

        problem=0
        type_entree_xor = self.combo_entree_xor.get_active()
        if type_entree_xor:
            txt_entree_xor=re.sub('[\s]+', ' ', txt_entree_xor)            # Remplacer tout les caractères d'espacement par des espaces
            txt_entree_xor=re.sub('[ ]+', ' ', txt_entree_xor)            # Enlever les espaces multiples
            txt_entree_xor=re.sub('^[ ]+', '', re.sub('[ ]+$', '', txt_entree_xor))    # Enlever les espaces en début et fin de chaine

            if re.compile("[^ \d]+", re.MULTILINE).search(txt_entree_xor):
                self.warnDialog("Erreur de saisie !\n\nUne code décimal ne peux contenir que des chiffres...")
                problem=1
            elif int(max(txt_entree_xor.split(' '))) > 255:
                self.warnDialog("Erreur de saisie !\n\nUne valeur décimale ne peux pas dépasser 255...")
                problem=1
            else: txt_entree_xor=txt_entree_xor.split(' ')
        if not problem:
            for i in txt_entree_xor:
                if not self.combo_entree_xor.get_active():         # ASCII
                    if not self.combo_sortie_xor.get_active():
                        data += chr(ord(key[c])^ord(i))        # > ASCII
                    else:
                        data += str(ord(key[c])^ord(i))+' '    # > DECIMAL
                else:                            # DECIMAL
                    if not self.combo_sortie_xor.get_active():
                        data += chr(ord(key[c])^int(i))        # > ASCII
                    else:
                        data += str(ord(key[c])^int(i))+' '    # > DECIMAL
                c += 1
                if(c >= len(key)):
                    c = 0

            try: data.decode('utf-8')
            except UnicodeDecodeError:
                self.warnDialog("Affichage en ASCII impossible !\n\nLe code contient sûrement des caractères non imprimables...")
                # si ascii > decimal
                if not self.combo_sortie_xor.get_active():
                    self.combo_sortie_xor.set_active(1)
                    txtbuf_sortie_xor.insert(start_iter_sortie_xor, ' '.join(str(ord(i)) for i in data))
            else:
                if '\0' in data:
                    self.warnDialog("Affichage en ASCII impossible !\n\nLe code contient sûrement des caractères non imprimables...")
                    # si ascii > decimal
                    if not self.combo_sortie_xor.get_active():
                        self.combo_sortie_xor.set_active(1)
                        txtbuf_sortie_xor.insert(start_iter_sortie_xor, ' '.join(str(ord(i)) for i in data))
                else:
                    if not self.combo_sortie_xor.get_active():
                        txtbuf_sortie_xor.insert(start_iter_sortie_xor, ''.join(data))
                    else:
                        txtbuf_sortie_xor.insert(start_iter_sortie_xor, ''.join(data).rstrip(' '))

# VIGENERE

    def vigenere(self, widget, mode):
        """Chiffre de Vigenère"""
        # Buffer et texte d'entrée
        txtbuf_entree_vigenere = self.textview_entree_vigenere.get_buffer()
        txt_entree_vigenere = txtbuf_entree_vigenere.get_text(txtbuf_entree_vigenere.get_start_iter(),txtbuf_entree_vigenere.get_end_iter())

        # Buffer, début et fin de buffer d'entrée
        txtbuf_entree_vigenere = self.textview_entree_vigenere.get_buffer()
        start_iter_entree_vigenere = txtbuf_entree_vigenere.get_start_iter()
        end_iter_entree_vigenere = txtbuf_entree_vigenere.get_end_iter()

        # Buffer, début et fin de buffer de sortie
        txtbuf_sortie_vigenere = self.textview_sortie_vigenere.get_buffer()
        start_iter_sortie_vigenere = txtbuf_sortie_vigenere.get_start_iter()
        end_iter_sortie_vigenere = txtbuf_sortie_vigenere.get_end_iter()

        # Suppression du texte de sortie
        txtbuf_sortie_vigenere.delete(start_iter_sortie_vigenere, end_iter_sortie_vigenere)

        str_tocrypt=re.sub('[^A-Z\s]','',txt_entree_vigenere.upper())
        txtbuf_entree_vigenere.delete(start_iter_entree_vigenere, end_iter_entree_vigenere)
        txtbuf_entree_vigenere.insert(start_iter_entree_vigenere, str_tocrypt)

        cle=re.sub('[^A-Z]','',self.entry_key_vigenere.get_text().upper())
        self.entry_key_vigenere.set_text(cle)

        i=0
        esp_sum=0
        str_crypted=''
        while i<=len(str_tocrypt)-1:
            if str_tocrypt[i] not in (' ','\t','\n','\r','\f','\v'):
                let_interm=cle[i-(i/len(cle))*len(cle)-(esp_sum-(esp_sum/len(cle))*len(cle))]
                decalage=ord(let_interm)-65

                if mode:    # chiffrement
                    if ord(str_tocrypt[i])+decalage>90:
                        let_new=chr(ord(str_tocrypt[i])+decalage-26)
                    else:
                        let_new=chr(ord(str_tocrypt[i])+decalage)
                elif not mode:    # dechiffrement
                    if ord(str_tocrypt[i])-decalage<65:
                        let_new=chr(ord(str_tocrypt[i])-decalage+26)
                    else:
                        let_new=chr(ord(str_tocrypt[i])-decalage)

                str_crypted+=let_new
            else:
                str_crypted+=str_tocrypt[i]
                esp_sum+=1
            i=i+1
        txtbuf_sortie_vigenere.insert(start_iter_sortie_vigenere, str_crypted)

# AUTRES

    def runAsRoot(self, parent, module):
        for su_gui_cmd in ['gksu','kdesu','ktsuss','beesu','gnome-terminal','xterm','']:
            if getoutput("which "+su_gui_cmd): break
        if su_gui_cmd:
            if not "term" in su_gui_cmd: os.system(su_gui_cmd+' '+module)
            else:
                # En dernier recour, ouvrir un nouveau gnome-terminal/xterm et utiliser sudo/su
                if getoutput("which sudo"): os.system(su_gui_cmd+' -e "sudo '+module+'"')
                else: os.system(su_gui_cmd+' -e "su -c '+module+'"')
        else: print "rien"

    def requete_http(self, cnx, method, url, data = ""):
        """Gestion des requetes HTTP"""
        if method.upper() == "POST":
            headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.3) Gecko/20100401","Content-Type" : "application/x-www-form-urlencoded"}
            head, ret = cnx.request(url, method.upper(), urlencode(data), headers = headers)
        elif method.upper() == "GET":
            headers = {"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.3) Gecko/20100401"}
            head, ret = cnx.request(url, method.upper(), urlencode(data), headers = headers)
        return ret

# Interface graphique :

    def quitDialog(self, widget, data):
        if self.yesnoDialog("Voulez-vous vraiment quitter\nla Free-knowledge Toolbox ?"): delete()
        else: return 1

    def yesnoDialog(self, message):
        # Creation de la boite de message
        # Type : Question -> gtk.MESSAGE_QUESTION
        # Boutons : 1 OUI, 1 NON -> gtk.BUTTONS_YES_NO
        question = gtk.MessageDialog(self.fenetre,
                                     gtk.DIALOG_MODAL,
                                     gtk.MESSAGE_QUESTION,
                                     gtk.BUTTONS_YES_NO,
                                     message)

        # Affichage et attente d une reponse
        reponse = question.run()
        question.destroy()
        if reponse == gtk.RESPONSE_YES: return 1
        elif reponse == gtk.RESPONSE_NO: return 0

    def msgbox(self, message, type_msg=0):
        about = gtk.MessageDialog(self.fenetre,
                                  gtk.DIALOG_MODAL,
                                  gtk.MESSAGE_WARNING if type_msg else gtk.MESSAGE_INFO,
                                  gtk.BUTTONS_OK,
                                  message)
        about.run() # Affichage de la boite de message
        about.destroy() # Destruction de la boite de message

    def warnDialog(self, message):
        about = gtk.MessageDialog(self.fenetre,
                                  gtk.DIALOG_MODAL,
                                  gtk.MESSAGE_WARNING,
                                  gtk.BUTTONS_OK,
                                  message)
        about.run() # Affichage de la boite de message
        about.destroy() # Destruction de la boite de message

    def infoDialog(self, message):
        about = gtk.MessageDialog(self.fenetre,
                                  gtk.DIALOG_MODAL,
                                  gtk.MESSAGE_INFO,
                                  gtk.BUTTONS_OK,
                                  message)
        about.run() # Affichage de la boite de message
        about.destroy() # Destruction de la boite de message

    def enrResultCouchesRVB(self, widget, data):
        dialogue = gtk.FileChooserDialog("Enregister l'image",None,gtk.FILE_CHOOSER_ACTION_SAVE,
                                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,    # bouton annuler
                                          gtk.STOCK_SAVE, gtk.RESPONSE_OK))    # bouton enregistrer
        dialogue.set_default_response(gtk.RESPONSE_OK)
        dialogue.set_current_name('Resultat_stega.png')

        filtre = gtk.FileFilter()
        filtre.set_name("Images *.png")
        filtre.add_mime_type("image/png")
        filtre.add_pattern("*.png")
        dialogue.add_filter(filtre)

        filtre = gtk.FileFilter()
        filtre.set_name("All files")
        filtre.add_pattern("*")
        dialogue.add_filter(filtre)

        reponse = dialogue.run()
        if reponse == gtk.RESPONSE_OK:
            sortie=dialogue.get_filename()
        elif reponse == gtk.RESPONSE_CANCEL:
            sortie=0
        else:
            sortie=0

        dialogue.destroy()

        if sortie != 0:
            os.system("cp \"%s/tmp/result_stega.png\" \"" % FKTB_PATH + sortie + "\"")

    def dialogueFichierStega(self, parent):
        # On efface les éventuelles images
        for fils in self.scrolled_img_result_c_rgb.get_children():
            self.scrolled_img_result_c_rgb.remove(fils)
        for fils in self.scrolled_img_orig_c_rgb.get_children():
            self.scrolled_img_orig_c_rgb.remove(fils)
        if self.btn_radio_hide_c_rgb.get_active():
            # Buffer et texte d'entrée
            txtbuf_texte_c_rgb = self.textview_texte_c_rgb.get_buffer()
            self.texte_c_rgb = txtbuf_texte_c_rgb.get_text(txtbuf_texte_c_rgb.get_start_iter(),txtbuf_texte_c_rgb.get_end_iter())

            if self.texte_c_rgb != "":
                dialogue = gtk.FileChooserDialog("Ouvrir une image",None,gtk.FILE_CHOOSER_ACTION_OPEN,
                                                 (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,    # bouton annuler
                                                  gtk.STOCK_OPEN, gtk.RESPONSE_OK))    # bouton ouvrir
                dialogue.set_default_response(gtk.RESPONSE_OK)

                filtre = gtk.FileFilter()
                filtre.set_name("All files")
                filtre.add_pattern("*")
                dialogue.add_filter(filtre)

                reponse = dialogue.run()
                if reponse == gtk.RESPONSE_OK:
                    sortie=dialogue.get_filename()
                elif reponse == gtk.RESPONSE_CANCEL:
                    sortie=0
                else:
                    sortie=0

                dialogue.destroy()
                if sortie != 0:
                    self.entry_img_c_rgb.set_text(sortie)
                    self.img_orig = gtk.Image()
                    self.img_orig.set_from_file(sortie)
                    self.scrolled_img_orig_c_rgb.add_with_viewport(self.img_orig)
                    self.img_orig.show()

                    self.boite_apercu_c_rgb.show()
                    self.boite8_c_rgb.show()
                    self.hideMsg()

                else:
                    self.cleanCouchesRVB(1) # 1 ou n'importe quoi pour ne pas supprimer le texte
            else:
                self.warnDialog("Veuillez saisir du texte !")
        else: #elif self.btn_radio_read_c_rgb.get_active():
            dialogue = gtk.FileChooserDialog("Ouvrir une image",None,gtk.FILE_CHOOSER_ACTION_OPEN,
                                             (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, # bouton annuler
                                              gtk.STOCK_OPEN, gtk.RESPONSE_OK)) # bouton ouvrir
            dialogue.set_default_response(gtk.RESPONSE_OK)

            filtre = gtk.FileFilter()
            filtre.set_name("All files")
            filtre.add_pattern("*")
            dialogue.add_filter(filtre)

            reponse = dialogue.run()
            if reponse == gtk.RESPONSE_OK:
                sortie=dialogue.get_filename()
            elif reponse == gtk.RESPONSE_CANCEL:
                sortie=0
            else:
                sortie=0

            dialogue.destroy()
            if sortie != 0:
                #print "sortie != 0"
                self.entry_img_c_rgb.set_text(sortie)
                self.img_orig = gtk.Image()
                self.img_orig.set_from_file(sortie)
                self.scrolled_img_orig_c_rgb.add_with_viewport(self.img_orig)
                self.img_orig.show()

                self.boite_apercu_c_rgb.show()
                self.boite8_c_rgb.hide()

                self.readMsg()
            else:
                self.cleanCouchesRVB()

    def dialogueHasherFichier(self, parent):
        last_path = self.entry_fichier_hash.get_text()
        dialogue = gtk.FileChooserDialog("Hasher un fichier",None,gtk.FILE_CHOOSER_ACTION_OPEN,
                                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,    # bouton annuler
                                          gtk.STOCK_OPEN, gtk.RESPONSE_OK))    # bouton ouvrir
        dialogue.set_default_response(gtk.RESPONSE_OK)

        filtre = gtk.FileFilter()
        filtre.set_name("All files")
        filtre.add_pattern("*")
        dialogue.add_filter(filtre)

        reponse = dialogue.run()
        if reponse == gtk.RESPONSE_OK:
            sortie=dialogue.get_filename()
        elif reponse == gtk.RESPONSE_CANCEL:
            sortie=0
        else:
            sortie=0

        dialogue.destroy()
        if sortie != 0:
            if sortie != last_path:
                self.entry_fichier_hash.set_text(sortie)
                self.entry_result_hash.set_text("")

    def dialogueOuvrirPieceJ(self, parent):
        dialogue = gtk.FileChooserDialog("Ouvrir un fichier",None,gtk.FILE_CHOOSER_ACTION_OPEN,
                                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,    # bouton annuler
                                          gtk.STOCK_OPEN, gtk.RESPONSE_OK))    # bouton ouvrir
        dialogue.set_default_response(gtk.RESPONSE_OK)

        filtre = gtk.FileFilter()
        filtre.set_name("All files")
        filtre.add_pattern("*")
        dialogue.add_filter(filtre)

        reponse = dialogue.run()
        if reponse == gtk.RESPONSE_OK:
            sortie=dialogue.get_filename()
        elif reponse == gtk.RESPONSE_CANCEL:
            sortie=0
        else:
            sortie=0

        dialogue.destroy()
        if sortie != 0:
            self.entry_mail_piece_j.set_text(sortie)

    def dialogueOuvrirStrings(self, parent):
        dialogue = gtk.FileChooserDialog("Ouvrir un fichier",None,gtk.FILE_CHOOSER_ACTION_OPEN,
                                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,    # bouton annuler
                                          gtk.STOCK_OPEN, gtk.RESPONSE_OK))    # bouton ouvrir
        dialogue.set_default_response(gtk.RESPONSE_OK)

        filtre = gtk.FileFilter()
        filtre.set_name("All files")
        filtre.add_pattern("*")
        dialogue.add_filter(filtre)

        reponse = dialogue.run()
        if reponse == gtk.RESPONSE_OK:
            sortie=dialogue.get_filename()
        elif reponse == gtk.RESPONSE_CANCEL:
            sortie=0
        else:
            sortie=0

        dialogue.destroy()
        if sortie != 0:
            self.entry_strings.set_text(sortie)
            self.stringsFichier("")

    def dialogueOuvrirBin(self, parent):
        dialogue = gtk.FileChooserDialog("Ouvrir un fichier",None,gtk.FILE_CHOOSER_ACTION_OPEN,
                                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,    # bouton annuler
                                          gtk.STOCK_OPEN, gtk.RESPONSE_OK))    # bouton ouvrir
        dialogue.set_default_response(gtk.RESPONSE_OK)

        filtre = gtk.FileFilter()
        filtre.set_name("All files")
        filtre.add_pattern("*")
        dialogue.add_filter(filtre)

        reponse = dialogue.run()
        if reponse == gtk.RESPONSE_OK:
            sortie=dialogue.get_filename()
        elif reponse == gtk.RESPONSE_CANCEL:
            sortie=0
        else:
            sortie=0

        dialogue.destroy()
        if sortie != 0:
            self.entry_bin_asm.set_text(sortie)

    def dialogueOuvrirOpNot(self, parent):
        dialogue = gtk.FileChooserDialog("Ouvrir un fichier",None,gtk.FILE_CHOOSER_ACTION_OPEN,
                                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,    # bouton annuler
                                          gtk.STOCK_OPEN, gtk.RESPONSE_OK))    # bouton ouvrir
        dialogue.set_default_response(gtk.RESPONSE_OK)

        filtre = gtk.FileFilter()
        filtre.set_name("All files")
        filtre.add_pattern("*")
        dialogue.add_filter(filtre)

        reponse = dialogue.run()
        if reponse == gtk.RESPONSE_OK: sortie=dialogue.get_filename()
        else: sortie=0

        dialogue.destroy()
        if sortie:
            self.btn_save_out_op_not.set_sensitive(False)
            thread.start_new_thread(self.opNot, (sortie,))
        else:
            self.btn_save_out_op_not.set_sensitive(False)
            self.label_in_file_op_not.set_text("Fichier d'entrée :")
            self.entry_in_file_op_not.set_text('')
            self.label_out_file_op_not.set_text("Fichier en sortie :")
            self.progressbarOpNot.set_fraction(0)
            self.progressbarOpNot.set_text('')

    def aide_regex(self, widget):
        self.aide_regex_win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.aide_regex_win.set_transient_for(self.fenetre)
        self.aide_regex_win.set_resizable(True)
        self.aide_regex_win.set_title("Aide regex") # Titre de la fenêtre
        self.aide_regex_win.set_icon_from_file("%s/images/icone.png" % FKTB_PATH) # Spécifie une icône
        self.aide_regex_win.set_position(gtk.WIN_POS_CENTER_ON_PARENT) # Centrer la fenêtre au lancement
        self.aide_regex_win.set_border_width(0)
        self.aide_regex_win.set_size_request(700, 300) # Taille de la fenêtre

        vbox = gtk.VBox(False, 0)
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw, True, True, 0)

        store = gtk.ListStore(str, str)

        regex_elements = [('.', 'Correspond à tout caractère.'),
                          ('*', 'Correspond à zéro ou plusieurs répétitions du caractère ou de l\'expression précédente.'),
                          ('+', 'Correspond à une ou plusieurs répétitions du caractère ou de l\'expression précédente.'),
                          ('?', 'Correspond à zéro ou une répétition du caractère ou de l\'expression précédente.'),
                          ('^', 'Correspond au début de la chaîne.'),
                          ('$', 'Correspond à la fin de la chaîne.'),
                          ('\\A', 'Correspond uniquement au début de la chaîne.'),
                          ('\\B', 'Correspond à la chaîne vide, mais seulement quand elle n\'est pas au début ou en fin de chaîne.'),
                          ('\\b', 'Correspond à la chaîne vide, mais seulement au début ou en fin de chaîne.'),
                          ('\\d', 'Correspond à n\'importe quel chiffre décimal, ce qui équivaut à [0-9].'),
                          ('\\D', 'Correspond à tout caractère non numérique, ce qui équivaut à [^0-9].'),
                          ('\\s', 'Correspond à tout caractère d\'espacement, ce qui équivaut à [ \\t\\n\\r\\f\\v].'),
                          ('\\S', 'Correspond à tout caractère non-blanc, ce qui équivaut à [^ \\t\\n\\r\\f\\v].'),
                          ('\\w', 'Correspond à tout caractère alphanumérique, ce qui équivaut à [a-zA-Z0-9_].'),
                          ('\\W', 'Correspond à tout caractère non alphanumérique, ce qui équivaut à [^a-zA-Z0-9_].'),
                          ('\\z', 'Correspond uniquement à la fin de la chaîne.'),
                          ('\\\\', 'Correspond à une barre oblique inverse littérale.'),
                          ('??', '? retournant la correspondance la plus courte possible.'),
                          ('*?', '* retournant la correspondance la plus courte possible.'),
                          ('+?', '+ retournant la correspondance la plus courte possible.')]

        for act in regex_elements: store.append(act)

        treeView = gtk.TreeView(store)
        treeView.set_rules_hint(True)
        sw.add(treeView)

        treeView.append_column(gtk.TreeViewColumn("Symbole", gtk.CellRendererText(), text=0))
        treeView.append_column(gtk.TreeViewColumn("Définition", gtk.CellRendererText(), text=1))

        self.aide_regex_win.add(vbox)
        self.aide_regex_win.show_all()

    def about(self, widget):
        about_win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        about_win.set_transient_for(self.fenetre)
        about_win.set_resizable(False)
        about_win.set_title("À Propos ...") # Titre de la fenêtre
        about_win.set_icon_from_file("%s/images/icone.png" % FKTB_PATH) # Spécifie une icône
        about_win.set_position(gtk.WIN_POS_CENTER_ON_PARENT) # Centrer la fenêtre au lancement
        about_win.set_border_width(0)
        about_win.set_size_request(430, 340) # Taille de la fenêtre

        fixed_about = gtk.Fixed()

        img_a_propos = gtk.Image()
        img_a_propos.set_from_file("%s/images/a_propos.png" % FKTB_PATH)
        img_a_propos.show()

        fixed_about.put(img_a_propos, 0, 0)

        version = gtk.Label("v0.2.3")
        fixed_about.put(version, 20, 80)

        lab_auteurs = gtk.Label("Auteurs :\n\n  Julien Deudon (initbrain)\n  Geoffrey Robert (mks)")
        fixed_about.put(lab_auteurs, 20, 160)

        lab_contrib = gtk.Label("Contributeurs :\n\n  Laura Henrion\n  Mathieu Bonnet\n  Sylvain Ciacnoghi (TheStyx)")
        fixed_about.put(lab_contrib, 220, 160)

        lab_contact = gtk.Label("Site :\nMail :")
        lab_contact.set_alignment(0,0)
        lab_contact.set_size_request(250,100)
        fixed_about.put(lab_contact, 180, 290)

        boite_ev_site = gtk.EventBox()
        boite_ev_site.set_visible_window(False)
        fixed_about.put(boite_ev_site, 225, 290)
        boite_ev_site.show()

        lab_site = gtk.Label("www.free-knowledge.net")
        lab_site.set_alignment(0,0)
        lab_site.set_size_request(250,18)

        boite_ev_site.add(lab_site)
        boite_ev_site.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        boite_ev_site.connect("button_press_event", lambda w,e: webbrowser.open("http://www.free-knowledge.net"))

        lab_mail = gtk.Label("contact@free-knowledge.net")
        lab_mail.set_alignment(0,0)
        lab_mail.set_size_request(250,18)
        lab_mail.set_selectable(True)
        fixed_about.put(lab_mail, 225, 307)

        lab_copy = gtk.Label("Copyleft !© 2012 :")
        lab_copy.set_alignment(0,0)
        lab_copy.set_size_request(135,25)
        fixed_about.put(lab_copy, 20, 250)

        boite_ev_gpl = gtk.EventBox()
        boite_ev_gpl.set_visible_window(False)
        fixed_about.put(boite_ev_gpl, 20, 270)
        boite_ev_gpl.show()

        gpl = gtk.Image()
        gpl.set_from_file("%s/images/logo_gpl_v3.png" % FKTB_PATH)
        boite_ev_gpl.add(gpl)
        gpl.show()

        boite_ev_gpl.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        boite_ev_gpl.connect("button_press_event", lambda w,e: webbrowser.open("http://www.gnu.org/licenses/gpl-3.0.txt"))
        about_win.add(fixed_about)

        about_win.show_all()

    def menuChoice(self, parent):
        try:
            choix = self.treestore_menu.get_value(self.treeview_menu.get_selection().get_selected()[1], 0)
        except TypeError:
            pass
        else:
            #TODO modules en développement ...
            if choix in ["ARP",
                         "ICMP/SYN Scan",
                         "Whois",
                         "Dig",
                         "IPv4 Subnets",
                         "IPv6 Subnets",
                         "tcpdump",
                         "tcptrack",
                         "tcpflow",
                         "Connections Monitoring"]:
                self.bloc_tabs.set_current_page(0)
            else:
                for fils in self.bloc_tabs.get_children():
                    if choix == self.bloc_tabs.get_tab_label_text(fils):
                        self.bloc_tabs.set_current_page(self.bloc_tabs.page_num(fils))

    def tabBuilder(self): # Créer un nouveau bloc-notes, définir la position des onglets
    # Notebook du contenu
        self.bloc_tabs = gtk.Notebook()
        self.bloc_tabs.set_show_border(False)
        self.bloc_tabs.show()

        # boite_all
        self.boite_all = gtk.HBox(False, 10)
        self.boite_all.pack_end(self.bloc_tabs, True, True, 0)
        self.boite_all.show()
        self.fenetre.add(self.boite_all)

        separateur_all = gtk.VSeparator()
        self.boite_all.pack_end(separateur_all, False, False, 0)
        separateur_all.show()

        # afficher les tabs -> 1, les cacher -> 0
        self.bloc_tabs.set_show_tabs(0)

        self.fenetre.show_all()

    def tabIndisp(self): # TAB Indisponible
    # Boites 1 & 2
        boite1_indisp = gtk.VBox(True, 5)
        boite1_indisp.show()
        boite2_indisp = gtk.HBox(True, 5)
        boite1_indisp.pack_start(boite2_indisp, False, False, 0)
        boite2_indisp.show()

        # label_titre_indisp
        label_titre_indisp = gtk.Label("")
        label_titre_indisp.set_markup("<big><b>module en cours de développement</b></big>")
        label_titre_indisp.set_alignment(0,5)
        boite2_indisp.pack_start(label_titre_indisp, False, False, 0)
        label_titre_indisp.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_indisp, gtk.Label("Indisponible"), -1)

    def tabAccueil(self): # TAB Accueil
    # Boites 1 & 2
        boite1_accueil = gtk.VBox(False, 5)
        boite1_accueil.show()
        boite2_accueil = gtk.HBox(False, 5)
        boite1_accueil.pack_start(boite2_accueil, False, False, 0)
        boite2_accueil.show()

        # label_titre_accueil
        label_titre_accueil = gtk.Label("")
        label_titre_accueil.set_markup("<big><b>Don't learn to Hack, hack to Learn ^^</b></big>")
        label_titre_accueil.set_alignment(0,0)
        boite2_accueil.pack_start(label_titre_accueil, False, False, 0)
        label_titre_accueil.show()

        # btn_a_propos
        btn_a_propos = gtk.Button("?")
        btn_a_propos.set_size_request(int(btn_a_propos.size_request()[0]*2),btn_a_propos.size_request()[1])
        boite2_accueil.pack_end(btn_a_propos, False, False, 0)
        btn_a_propos.connect("clicked", self.about)
        btn_a_propos.show()

        # separateur_accueil
        separateur_accueil = gtk.HSeparator()
        boite1_accueil.pack_start(separateur_accueil, False, False, 5)
        separateur_accueil.show()

        # label_desc_accueil
        label_desc_accueil = gtk.Label("")
        label_desc_accueil.set_markup("Plein écran : F11")
        label_desc_accueil.set_alignment(0.5,0)
        boite1_accueil.pack_start(label_desc_accueil, False, False, 0)
        label_desc_accueil.show()

        # On crée une boîte à évènement et on l'ajoute à la fenêtre principale
        boite_evenement_laptop = gtk.EventBox()

        # image_laptop
        image_laptop = gtk.Image()
        #        image_laptop.set_from_file("%s/images/laptop.png" % FKTB_PATH)
        #        image_laptop.set_pixel_size(10)
        pixbuf_laptop = gtk.gdk.pixbuf_new_from_file_at_size("%s/images/white_hat.svg" % FKTB_PATH, int(boite1_accueil.size_request()[0]), -1)
        image_laptop.set_from_pixbuf(pixbuf_laptop)
        boite_evenement_laptop.add(image_laptop)
        boite_evenement_laptop.set_visible_window(False)
        boite1_accueil.pack_start(boite_evenement_laptop, True, False, 0)
        image_laptop.show()
        boite_evenement_laptop.show()

        # Boites 3 & 4
        boite3_accueil = gtk.HBox(False, 0)
        boite1_accueil.pack_end(boite3_accueil, False, False, 0)
        boite3_accueil.show()
        boite4_accueil = gtk.VBox(False, 0)
        boite3_accueil.pack_start(boite4_accueil, False, False, 0)
        boite4_accueil.show()

        # # btn_check_update
        # btn_check_update = gtk.Button("Vérifier les mises à jour")
        # btn_check_update.set_size_request(int(btn_check_update.size_request()[0]*1.1),btn_check_update.size_request()[1])
        # boite4_accueil.pack_end(btn_check_update, False, False, 0)
        # btn_check_update.connect("clicked", lambda e: thread.start_new_thread(self.checkUpdate, ()))
        # btn_check_update.show()

        # On crée une boîte à évènement et on l'ajoute à la fenêtre principale
        boite_evenement_april = gtk.EventBox()

        # image_april
        image_april = gtk.Image()
        image_april.set_from_file("%s/images/logo_april.png" % FKTB_PATH)
        boite_evenement_april.add(image_april)
        image_april.show()

        # On relie une action à la boîte
        boite_evenement_april.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        boite_evenement_april.set_visible_window(False)
        boite_evenement_april.connect("button_press_event", lambda w,e: webbrowser.open("http://www.april.org"))
        boite3_accueil.pack_end(boite_evenement_april, False, False, 0)
        boite_evenement_april.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_accueil, gtk.Label("Accueil"), -1)

    def tabCesar(self): # TAB César
    # boites
        boite1_cesar = gtk.VBox(False, 5)
        boite1_cesar.show()

        boite2_cesar = gtk.HBox(False, 5)
        boite1_cesar.pack_start(boite2_cesar, False, False, 0)
        boite2_cesar.show()

        boite3_cesar = gtk.VBox(False, 5)
        boite2_cesar.pack_start(boite3_cesar, True, True, 0)
        boite3_cesar.show()

        boite4_cesar = gtk.VBox(False, 5)
        boite2_cesar.pack_start(boite4_cesar, False, False, 0)
        boite4_cesar.show()

        boite5_cesar = gtk.VBox(False, 0)
        boite2_cesar.pack_start(boite5_cesar, False, False, 0)
        boite5_cesar.show()

        boite6_cesar = gtk.HBox(False, 0)
        boite1_cesar.pack_start(boite6_cesar, False, False, 0)
        boite6_cesar.show()

        # label_alphabet_cesar
        label_alphabet_cesar = gtk.Label("Alphabet utilisé :")
        label_alphabet_cesar.set_alignment(0, 0)
        boite3_cesar.pack_start(label_alphabet_cesar, False, False, 0)
        label_alphabet_cesar.show()

        # self.entry_alphabet_cesar
        self.entry_alphabet_cesar = gtk.Entry()
        self.entry_alphabet_cesar.set_text("abcdefghijklmnopqrstuvwxyz")
        boite3_cesar.pack_start(self.entry_alphabet_cesar, True, True, 0)
        self.entry_alphabet_cesar.show()

        # label_rot_cesar
        label_rot_cesar = gtk.Label("Rotation :")
        label_rot_cesar.set_alignment(0, 0)
        boite4_cesar.pack_start(label_rot_cesar, False, False, 0)
        label_rot_cesar.show()

        # self.entry_rot_cesar
        self.entry_rot_cesar = gtk.Entry()
        self.entry_rot_cesar.set_text("13")
        self.entry_rot_cesar.set_size_request(30,self.entry_rot_cesar.size_request()[1])
        boite4_cesar.pack_start(self.entry_rot_cesar, True, True, 0)
        self.entry_rot_cesar.show()

        # self.btn_cesar
        self.btn_cesar = gtk.Button("ok")
        self.btn_cesar.set_size_request(int(self.btn_cesar.size_request()[0]*1.2),self.btn_cesar.size_request()[1])
        boite5_cesar.pack_end(self.btn_cesar, False, False, 0)
        self.btn_cesar.connect("clicked", self.checkCesar)
        self.btn_cesar.show()

        # self.btn_radio
        self.btn_radio_ch = gtk.RadioButton(None, "Chiffrer")
        boite6_cesar.pack_start(self.btn_radio_ch, True, False, 0)
        self.btn_radio_ch.show()

        self.btn_radio_dech_co = gtk.RadioButton(self.btn_radio_ch, "Déchiffrer (clé connue)")
        boite6_cesar.pack_start(self.btn_radio_dech_co, True, False, 0)
        self.btn_radio_dech_co.show()

        self.btn_radio_dech_inco = gtk.RadioButton(self.btn_radio_ch, "Décrypter (clé inconnue)")
        boite6_cesar.pack_start(self.btn_radio_dech_inco, True, False, 0)
        self.btn_radio_dech_inco.show()

        # separateur_cesar
        separateur_cesar = gtk.HSeparator()
        boite1_cesar.pack_start(separateur_cesar, False, False, 0)
        separateur_cesar.show()

        # label_entree_cesar
        label_entree_cesar = gtk.Label("Texte à chiffrer / déchiffrer :")
        label_entree_cesar.set_alignment(0,0)
        boite1_cesar.pack_start(label_entree_cesar, False, False, 0)
        label_entree_cesar.show()
        # scrollbar_entree
        scrolled_entree_cesar = gtk.ScrolledWindow()
        boite1_cesar.pack_start(scrolled_entree_cesar, True, True, 0)
        scrolled_entree_cesar.show()
        # self.textview_entree_cesar
        self.textview_entree_cesar = gtk.TextView()
        scrolled_entree_cesar.add(self.textview_entree_cesar)
        scrolled_entree_cesar.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_entree_cesar.show()

        # label_sortie_cesar
        label_sortie_cesar = gtk.Label("Résultat :")
        label_sortie_cesar.set_alignment(0,0)
        boite1_cesar.pack_start(label_sortie_cesar, False, False, 0)
        label_sortie_cesar.show()
        # scrollbar_sortie
        scrolled_sortie_cesar = gtk.ScrolledWindow()
        boite1_cesar.pack_start(scrolled_sortie_cesar, True, True, 0)
        scrolled_sortie_cesar.show()
        # self.textview_sortie_cesar
        self.textview_sortie_cesar = gtk.TextView()
        self.textview_sortie_cesar.set_editable(False)
        scrolled_sortie_cesar.add(self.textview_sortie_cesar)
        scrolled_sortie_cesar.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_sortie_cesar.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_cesar, gtk.Label("Chiffre de César"), -1)

    def tabSubstMonoAlpha(self): # TAB Substitution mono-alphabétique
    # boites
        boite1_substma = gtk.VBox(False, 5)
        boite1_substma.show()
        boite2_substma = gtk.HBox(False, 5)
        boite1_substma.pack_start(boite2_substma, False, False, 0)
        boite2_substma.show()
        boite3_substma = gtk.VBox(False, 0)
        boite2_substma.pack_start(boite3_substma, True, True, 0)
        boite3_substma.show()
        boite4_substma = gtk.VBox(False, 5)
        boite2_substma.pack_start(boite4_substma, False, False, 0)
        boite4_substma.show()

        # label1_substma
        label1_substma = gtk.Label("Alphabet 1 :")
        label1_substma.set_alignment(0, 0)
        boite3_substma.pack_start(label1_substma, False, False, 0)
        label1_substma.show()

        # self.entry_alphabet2_substma
        self.entry_alphabet1_substma = gtk.Entry()
        self.entry_alphabet1_substma.set_text("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        boite3_substma.pack_start(self.entry_alphabet1_substma, True, True, 5)
        self.entry_alphabet1_substma.show()

        # label2_substma
        label2_substma = gtk.Label("Alphabet 2 :")
        label2_substma.set_alignment(0, 0)
        boite3_substma.pack_start(label2_substma, False, False, 0)
        label2_substma.show()

        # self.entry_alphabet2_substma
        self.entry_alphabet2_substma = gtk.Entry()
        self.entry_alphabet2_substma.set_text("9876543210ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba")
        boite3_substma.pack_start(self.entry_alphabet2_substma, True, True, 5)
        self.entry_alphabet2_substma.show()

        # bouton_substma
        bouton_substma = gtk.Button("ok")
        bouton_substma.set_size_request(int(bouton_substma.size_request()[0]*1.2),bouton_substma.size_request()[1])
        boite4_substma.pack_start(bouton_substma, False, False, 20)
        bouton_substma.connect("clicked", self.checkSubstMonoAlpha)
        bouton_substma.show()

        # separateur_substma
        separateur_substma = gtk.HSeparator()
        boite1_substma.pack_start(separateur_substma, False, False, 0)
        separateur_substma.show()

        # label_entree_substma
        label_entree_substma = gtk.Label("Texte à substituer :")
        label_entree_substma.set_alignment(0,0)
        boite1_substma.pack_start(label_entree_substma, False, False, 0)
        label_entree_substma.show()
        # scrollbar_entree_substma
        scrolled_entree_substma = gtk.ScrolledWindow()
        boite1_substma.pack_start(scrolled_entree_substma, True, True, 0)
        scrolled_entree_substma.show()
        # self.textview_entree_substma
        self.textview_entree_substma = gtk.TextView()
        scrolled_entree_substma.add(self.textview_entree_substma)
        scrolled_entree_substma.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_entree_substma.show()

        # label_sortie_substma
        label_sortie_substma = gtk.Label("Résultat :")
        label_sortie_substma.set_alignment(0,0)
        boite1_substma.pack_start(label_sortie_substma, False, False, 0)
        label_sortie_substma.show()
        # scrollbar_sortie_substma
        scrolled_sortie_substma = gtk.ScrolledWindow()
        boite1_substma.pack_start(scrolled_sortie_substma, True, True, 0)
        scrolled_sortie_substma.show()
        # self.textview_sortie_substma
        self.textview_sortie_substma = gtk.TextView()
        self.textview_sortie_substma.set_editable(False)
        scrolled_sortie_substma.add(self.textview_sortie_substma)
        scrolled_sortie_substma.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_sortie_substma.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_substma, gtk.Label("Substitution\nmono-alphabétique"), -1)

    def tabHash(self): # TAB Hash
    # boite 1
        boite1_hash = gtk.VBox(False, 5)
        boite1_hash.show()

        # label1_hash
        label1_hash = gtk.Label("Fonction de Hashage :")
        label1_hash.set_alignment(0, 0)
        boite1_hash.pack_start(label1_hash, False, False, 0)
        label1_hash.show()

        # boite 2
        boite2_hash = gtk.HBox(False, 5)
        boite1_hash.pack_start(boite2_hash, False, False, 0)
        boite2_hash.show()

        # self.btn_radio_md5 ... sha1, sha224, sha256, sha384 et sha512
        self.btn_radio_md5 = gtk.RadioButton(None, "md5")
        boite2_hash.pack_start(self.btn_radio_md5, True, False, 0)
        self.btn_radio_md5.show()

        self.btn_radio_sha1 = gtk.RadioButton(self.btn_radio_md5, "sha1")
        boite2_hash.pack_start(self.btn_radio_sha1, True, False, 0)
        self.btn_radio_sha1.show()

        self.btn_radio_sha224 = gtk.RadioButton(self.btn_radio_md5, "sha224")
        boite2_hash.pack_start(self.btn_radio_sha224, True, False, 0)
        self.btn_radio_sha224.show()

        self.btn_radio_sha256 = gtk.RadioButton(self.btn_radio_md5, "sha256")
        boite2_hash.pack_start(self.btn_radio_sha256, True, False, 0)
        self.btn_radio_sha256.show()

        self.btn_radio_sha384 = gtk.RadioButton(self.btn_radio_md5, "sha384")
        boite2_hash.pack_start(self.btn_radio_sha384, True, False, 0)
        self.btn_radio_sha384.show()

        self.btn_radio_sha512 = gtk.RadioButton(self.btn_radio_md5, "sha512")
        boite2_hash.pack_start(self.btn_radio_sha512, True, False, 0)
        self.btn_radio_sha512.show()

        # separateur
        separateur1_hash = gtk.HSeparator()
        boite1_hash.pack_start(separateur1_hash, False, False, 0)
        separateur1_hash.show()

        # self.btn_radio_text_hash
        self.btn_radio_text_hash = gtk.RadioButton(None, "Texte :")
        boite1_hash.pack_start(self.btn_radio_text_hash, False, False, 0)
        self.btn_radio_text_hash.show()
        # self.scrollbar_entree_hash
        scrolled_entree_hash = gtk.ScrolledWindow()
        scrolled_entree_hash.set_size_request(575,150)
        boite1_hash.pack_start(scrolled_entree_hash, True, True, 0)
        scrolled_entree_hash.show()
        # self.textview_entree_hash
        self.textview_entree_hash = gtk.TextView()
        scrolled_entree_hash.add(self.textview_entree_hash)
        scrolled_entree_hash.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_entree_hash.show()

        # self.btn_radio_fichier_hash
        self.btn_radio_fichier_hash = gtk.RadioButton(self.btn_radio_text_hash, "Fichier :")
        boite1_hash.pack_start(self.btn_radio_fichier_hash, False, False, 0)
        self.btn_radio_fichier_hash.show()

        # boite 3
        boite3_hash = gtk.HBox(False, 5)
        boite1_hash.pack_start(boite3_hash, False, False, 0)
        boite3_hash.show()

        # self.entry_fichier_hash
        self.entry_fichier_hash = gtk.Entry()
        self.entry_fichier_hash.set_editable(False)
        boite3_hash.pack_start(self.entry_fichier_hash, True, True, 0)
        self.entry_fichier_hash.show()
        # self.btn_fichier_hash
        self.btn_fichier_hash = gtk.Button("Ouvrir")
        self.btn_fichier_hash.set_size_request(int(self.btn_fichier_hash.size_request()[0]*1.1),self.btn_fichier_hash.size_request()[1])
        boite3_hash.pack_start(self.btn_fichier_hash, False, False, 0)
        self.btn_fichier_hash.connect("clicked", self.dialogueHasherFichier)
        self.btn_fichier_hash.show()

        # Désactivation de la partie fichier par défaut
        self.entry_fichier_hash.set_sensitive(False)
        self.btn_fichier_hash.set_sensitive(False)

        # separateur
        separateur2_hash = gtk.HSeparator()
        boite1_hash.pack_start(separateur2_hash, False, False, 0)
        separateur2_hash.show()

        # boite 4
        boite4_hash = gtk.HBox(False, 5)
        boite1_hash.pack_start(boite4_hash, False, False, 0)
        boite4_hash.show()

        # self.btn_calc_hash
        self.btn_calc_hash = gtk.Button("Calculer")
        self.btn_calc_hash.set_size_request(int(self.btn_calc_hash.size_request()[0]*1.1),self.btn_calc_hash.size_request()[1])
        self.btn_calc_hash.connect("clicked", self.calcHash)
        boite4_hash.pack_start(self.btn_calc_hash, True, False, 0)
        self.btn_calc_hash.show()

        # self.img_calc_hash
        buf_anim_hash = gtk.gdk.PixbufAnimation("%s/images/attente.gif" % FKTB_PATH)
        self.img_calc_hash = gtk.Image()
        self.img_calc_hash.set_from_animation(buf_anim_hash)
        boite4_hash.pack_start(self.img_calc_hash, True, False, 0)

        # self.label_result_hash
        self.label_result_hash = gtk.Label("Résultat :")
        self.label_result_hash.set_alignment(0,0)
        boite1_hash.pack_start(self.label_result_hash, False, False, 0)
        self.label_result_hash.show()

        # self.entry_result_hash
        self.entry_result_hash = gtk.Entry()
        self.entry_result_hash.set_editable(False)
        boite1_hash.pack_start(self.entry_result_hash, False, False, 0)
        self.entry_result_hash.show()

        # On vide le champ résultat dès changement d'une option
        self.btn_radio_md5.connect("toggled", self.cleanHash)
        self.btn_radio_sha1.connect("toggled", self.cleanHash)
        self.btn_radio_sha224.connect("toggled", self.cleanHash)
        self.btn_radio_sha256.connect("toggled", self.cleanHash)
        self.btn_radio_sha384.connect("toggled", self.cleanHash)
        self.btn_radio_sha512.connect("toggled", self.cleanHash)
        self.btn_radio_text_hash.connect("toggled", self.cleanHash, 1)

        # Affichage
        self.bloc_tabs.insert_page(boite1_hash, gtk.Label("Calcul d'empreintes"), -1)

    def tabmd5(self): # TAB md5
    # boite1_md5
        boite1_md5 = gtk.VBox(False, 5)
        boite1_md5.show()

        # label1_md5
        label1_md5 = gtk.Label("Utiliser :")
        label1_md5.set_alignment(0, 0)
        boite1_md5.pack_start(label1_md5, False, False, 0)
        label1_md5.show()

        # Boites
        boite_site_md5 = gtk.HBox(False, 0)
        boite1_md5.pack_start(boite_site_md5, False, False, 0)
        boite_site_md5.show()
        boite_col1_md5 = gtk.VBox(False, 0)
        boite_site_md5.pack_start(boite_col1_md5, True, True, 0)
        boite_col1_md5.show()
        boite_col2_md5 = gtk.VBox(False, 0)
        boite_site_md5.pack_start(boite_col2_md5, True, True, 0)
        boite_col2_md5.show()
        boite_col3_md5 = gtk.VBox(False, 0)
        boite_site_md5.pack_start(boite_col3_md5, True, True, 0)
        boite_col3_md5.show()

        boite2_md5 = gtk.HBox(False, 5)
        boite1_md5.pack_start(boite2_md5, False, False, 5)
        boite2_md5.show()

        # self.checkbtn_gromweb
        self.checkbtn_gromweb = gtk.CheckButton("md5.gromweb.com")
        boite_col1_md5.pack_start(self.checkbtn_gromweb, False, False, 0)
        self.checkbtn_gromweb.set_active(True)
        self.checkbtn_gromweb.show()

        # self.checkbtn_onlinehashcrack
        self.checkbtn_onlinehashcrack = gtk.CheckButton("onlinehashcrack.com")
        boite_col1_md5.pack_start(self.checkbtn_onlinehashcrack, False, False, 0)
        self.checkbtn_onlinehashcrack.set_active(True)
        self.checkbtn_onlinehashcrack.show()

        # self.checkbtn_c0llision
        self.checkbtn_c0llision = gtk.CheckButton("c0llision.net")
        boite_col1_md5.pack_start(self.checkbtn_c0llision, False, False, 0)
        self.checkbtn_c0llision.set_active(True)
        self.checkbtn_c0llision.show()

        # self.checkbtn_xanadrel
        self.checkbtn_xanadrel = gtk.CheckButton("xanadrel.99k.org")
        boite_col2_md5.pack_start(self.checkbtn_xanadrel, False, False, 0)
        self.checkbtn_xanadrel.set_active(True)
        self.checkbtn_xanadrel.show()

        # self.checkbtn_md5lookup
        self.checkbtn_md5lookup = gtk.CheckButton("md5-lookup.com")
        boite_col2_md5.pack_start(self.checkbtn_md5lookup, False, False, 0)
        self.checkbtn_md5lookup.set_active(True)
        self.checkbtn_md5lookup.show()

        # self.checkbtn_md5rednoize
        self.checkbtn_md5rednoize = gtk.CheckButton("md5.rednoize.com")
        boite_col2_md5.pack_start(self.checkbtn_md5rednoize, False, False, 0)
        self.checkbtn_md5rednoize.set_active(True)
        self.checkbtn_md5rednoize.show()

        # self.checkbtn_toolsbenramsey
        self.checkbtn_toolsbenramsey = gtk.CheckButton("tools.benramsey.com")
        boite_col3_md5.pack_start(self.checkbtn_toolsbenramsey, False, False, 0)
        self.checkbtn_toolsbenramsey.set_active(True)
        self.checkbtn_toolsbenramsey.show()

        # self.progressbarMd5
        self.progressbarMd5 = gtk.ProgressBar()
        boite2_md5.pack_start(self.progressbarMd5, True, True, 0)
        self.progressbarMd5.show()

        # self.btn_checkmd5
        self.btn_checkmd5 = gtk.Button("ok")
        self.btn_checkmd5.set_size_request(int(self.btn_checkmd5.size_request()[0]*1.2),self.btn_checkmd5.size_request()[1])
        self.btn_checkmd5.connect("clicked", self.mkThreadMd5)
        boite2_md5.pack_start(self.btn_checkmd5, False, False, 0)
        self.btn_checkmd5.show()

        # separateur_md5
        separateur_md5 = gtk.HSeparator()
        boite1_md5.pack_start(separateur_md5, False, False, 0)
        separateur_md5.show()

        # label_entree_md5
        label_entree_md5 = gtk.Label("Hash à rechercher :")
        label_entree_md5.set_alignment(0,0)
        boite1_md5.pack_start(label_entree_md5, False, False, 0)
        label_entree_md5.show()
        # scrollbar_entree
        scrolled_entree_md5 = gtk.ScrolledWindow()
        boite1_md5.pack_start(scrolled_entree_md5, True, True, 0)
        scrolled_entree_md5.show()
        # self.textview_entree_md5
        self.textview_entree_md5 = gtk.TextView()
        scrolled_entree_md5.add(self.textview_entree_md5)
        scrolled_entree_md5.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_entree_md5.show()

        # Buffer et texte d'entrée
        txtbuf_entree_md5 = self.textview_entree_md5.get_buffer()
        txt_entree_md5 = txtbuf_entree_md5.get_text(txtbuf_entree_md5.get_start_iter(),txtbuf_entree_md5.get_end_iter())

        # Buffer, début et fin de buffer pour le code source
        txtbuf_entree_md5 = self.textview_entree_md5.get_buffer()
        start_iter_entree_md5 = txtbuf_entree_md5.get_start_iter()
        end_iter_entree_md5 = txtbuf_entree_md5.get_end_iter()

        # Suppression du code source affiché
        txtbuf_entree_md5.delete(start_iter_entree_md5, end_iter_entree_md5)
        txtbuf_entree_md5.insert(start_iter_entree_md5, "f3883730022b105c691abc917fa17090:not_found...\n\nTestez la regex qui s'occupe de ne traiter que les hash !\n\nAppuyez sur ok dès maintenant ^^")

        # label_sortie_md5
        label_sortie_md5 = gtk.Label("Résultat :")
        label_sortie_md5.set_alignment(0,0)
        boite1_md5.pack_start(label_sortie_md5, False, False, 0)
        label_sortie_md5.show()
        # scrollbar_sortie
        scrolled_sortie_md5 = gtk.ScrolledWindow()
        boite1_md5.pack_start(scrolled_sortie_md5, True, True, 0)
        scrolled_sortie_md5.show()
        # self.textview_sortie_md5
        self.textview_sortie_md5 = gtk.TextView()
        self.textview_sortie_md5.set_editable(False)
        scrolled_sortie_md5.add(self.textview_sortie_md5)
        scrolled_sortie_md5.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_sortie_md5.show()

        # Ce cracker ne prend qu'un hash toute les 30 secondes : voir doc de l'API ci-dessous
        # -> http://blog.kalkulators.org/2011/08/28/le-cracker-v3-est-enfin-en-ligne/

        # Create button kalkulators
        #self.checkbtn_kalkulators = gtk.CheckButton("cracker.kalkulators.org")
        # Insert button kalkulators
        #self.fixed_md5.put(self.checkbtn_kalkulators, 25, 50)
        #self.checkbtn_kalkulators.set_active(True)
        #self.checkbtn_kalkulators.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_md5, gtk.Label("Recherche MD5"), -1)

    def tabRegex(self): # TAB regex
    # boites
        boite1_wregex = gtk.VBox(False, 5)
        boite1_wregex.show()

        # label_url_wregex
        label_url_wregex = gtk.Label("URL de la page WEB à parser :")
        label_url_wregex.set_alignment(0,0)
        boite1_wregex.pack_start(label_url_wregex, False, False, 0)
        label_url_wregex.show()

        # boite3_wregex
        boite3_wregex = gtk.HBox(False, 5)
        boite1_wregex.pack_start(boite3_wregex, False, False, 0)
        boite3_wregex.show()

        # self.entry_url_wregex
        self.entry_url_wregex = gtk.Entry()
        self.entry_url_wregex.set_text("http://www.perdu.com")
        boite3_wregex.pack_start(self.entry_url_wregex, True, True, 0)
        self.entry_url_wregex.show()

        # btn_wregex
        btn_wregex = gtk.Button("ok")
        btn_wregex.set_size_request(int(btn_wregex.size_request()[0]*1.2),btn_wregex.size_request()[1])
        boite3_wregex.pack_start(btn_wregex, False, False, 0)
        btn_wregex.connect("clicked", self.regex_http)
        btn_wregex.show()

        # label_reg_wregex
        label_reg_wregex = gtk.Label("Expression rationnelle à utiliser (python) :")
        label_reg_wregex.set_alignment(0,0)
        boite1_wregex.pack_start(label_reg_wregex, False, False, 0)
        label_reg_wregex.show()

        # boite4_wregex
        boite4_wregex = gtk.HBox(False, 5)
        boite1_wregex.pack_start(boite4_wregex, False, False, 0)
        boite4_wregex.show()

        # self.entry_reg_wregex
        self.entry_reg_wregex = gtk.Entry()
        self.entry_reg_wregex.set_text("<h1>([\w\\'\? ]+)</h1>")
        boite4_wregex.pack_start(self.entry_reg_wregex, True, True, 0)
        self.entry_reg_wregex.show()

        # btn_aide_wregex
        btn_aide_wregex = gtk.Button("?")
        btn_aide_wregex.set_size_request(btn_wregex.size_request()[0],btn_wregex.size_request()[1])
        boite4_wregex.pack_start(btn_aide_wregex, False, False, 0)
        btn_aide_wregex.connect("clicked", self.aide_regex)
        btn_aide_wregex.show()

        # separateur_wregex
        separateur_wregex = gtk.HSeparator()
        boite1_wregex.pack_start(separateur_wregex, False, False, 0)
        separateur_wregex.show()

        # label_source_wregex
        label_source_wregex = gtk.Label("Code source :")
        label_source_wregex.set_alignment(0,0)
        boite1_wregex.pack_start(label_source_wregex, False, False, 0)
        label_source_wregex.show()
        # scrollbar_source_wregex
        scrolled_source_wregex = gtk.ScrolledWindow()
        boite1_wregex.pack_start(scrolled_source_wregex, True, True, 0)
        scrolled_source_wregex.show()
        # self.textview_source_wregex
        self.textview_source_wregex = gtk.TextView()
        scrolled_source_wregex.add(self.textview_source_wregex)
        scrolled_source_wregex.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_source_wregex.show()

        # Buffer, début et fin de buffer pour le code source
        txtbuf_source_wregex = self.textview_source_wregex.get_buffer()
        start_iter_source_wregex = txtbuf_source_wregex.get_start_iter()
        end_iter_source_wregex = txtbuf_source_wregex.get_end_iter()

        # Suppression du code source affiché
        txtbuf_source_wregex.delete(start_iter_source_wregex, end_iter_source_wregex)
        txtbuf_source_wregex.insert(start_iter_source_wregex, "Exemple de regex : [\w\.\-]+@[\w\.\-]+\.[a-zA-Z]+\n-> recherche d'adresses mail")

        # self.label_result_wregex
        self.label_result_wregex = gtk.Label("Résultat :")
        self.label_result_wregex.set_alignment(0,0)
        boite1_wregex.pack_start(self.label_result_wregex, False, False, 0)
        self.label_result_wregex.show()
        # scrollbar_result_wregex
        scrolled_result_wregex = gtk.ScrolledWindow()
        boite1_wregex.pack_start(scrolled_result_wregex, True, True, 0)
        scrolled_result_wregex.show()
        # self.textview_result_wregex
        self.textview_result_wregex = gtk.TextView()
        self.textview_result_wregex.set_editable(False)
        scrolled_result_wregex.add(self.textview_result_wregex)
        scrolled_result_wregex.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_result_wregex.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_wregex, gtk.Label("Regex WEB"), -1)

    def tabStrings(self): # TAB strings
    # boites
        boite1_strings = gtk.VBox(False, 5)
        boite1_strings.show()
        boite2_strings = gtk.HBox(False, 5)
        boite1_strings.pack_start(boite2_strings, False, False, 0)
        boite2_strings.show()
        boite3_strings = gtk.VBox(False, 0)
        boite2_strings.pack_start(boite3_strings, True, True, 0)
        boite3_strings.show()
        boite4_strings = gtk.VBox(False, 0)
        boite2_strings.pack_start(boite4_strings, False, False, 0)
        boite4_strings.show()

        # label_strings
        label_strings = gtk.Label("Fichier :")
        label_strings.set_alignment(0, 0)
        boite3_strings.pack_start(label_strings, False, False, 0)
        label_strings.show()

        # self.entry_strings
        self.entry_strings = gtk.Entry()
        boite3_strings.pack_start(self.entry_strings, True, True, 5)
        self.entry_strings.show()

        # label_reg_strings
        label_reg_strings = gtk.Label("Regex (facultative) :")
        label_reg_strings.set_alignment(0, 0)
        boite3_strings.pack_start(label_reg_strings, False, False, 0)
        label_reg_strings.show()

        # self.entry_reg_strings
        self.entry_reg_strings = gtk.Entry()
        boite3_strings.pack_start(self.entry_reg_strings, True, True, 5)
        self.entry_reg_strings.show()

        # btn_reg_strings
        btn_reg_strings = gtk.Button("ok")
        btn_reg_strings.set_size_request(int(btn_reg_strings.size_request()[0]),btn_reg_strings.size_request()[1])
        btn_reg_strings.connect("clicked", self.stringsFichier)
        boite4_strings.pack_end(btn_reg_strings, False, False, 4)
        btn_reg_strings.show()

        # btn_file_strings
        btn_file_strings = gtk.Button("Ouvrir")
        btn_file_strings.set_size_request(int(btn_file_strings.size_request()[0]*1.1),btn_file_strings.size_request()[1])
        btn_file_strings.connect("clicked", self.dialogueOuvrirStrings)
        boite4_strings.pack_end(btn_file_strings, False, False, 20)
        btn_file_strings.show()

        # separateur_strings
        separateur_strings = gtk.HSeparator()
        boite1_strings.pack_start(separateur_strings, False, False, 0)
        separateur_strings.show()

        # self.label_result_strings
        self.label_result_strings = gtk.Label("Résultat :")
        self.label_result_strings.set_alignment(0,0)
        boite1_strings.pack_start(self.label_result_strings, False, False, 0)
        self.label_result_strings.show()
        # scrollbar_result_strings
        scrolled_result_strings = gtk.ScrolledWindow()
        boite1_strings.pack_start(scrolled_result_strings, True, True, 0)
        scrolled_result_strings.show()
        # self.textview_result_strings
        self.textview_result_strings = gtk.TextView()
        self.textview_result_strings.set_editable(False)
        scrolled_result_strings.add(self.textview_result_strings)
        scrolled_result_strings.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_result_strings.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_strings, gtk.Label("Commande strings"), -1)

    def tabMail(self): # TAB regex
    # boites
        boite1_mail = gtk.VBox(False, 5)
        boite1_mail.show()
        boite2_mail = gtk.HBox(False, 5)
        boite1_mail.pack_start(boite2_mail, False, False, 0)
        boite2_mail.show()
        boite3_mail = gtk.VBox(False, 5)
        boite2_mail.pack_start(boite3_mail, True, True, 0)
        boite3_mail.show()
        boite4_mail = gtk.VBox(False, 5)
        boite2_mail.pack_start(boite4_mail, True, True, 0)
        boite4_mail.show()

        # label_mail_smtp
        label_mail_smtp = gtk.Label("Serveur SMTP à utiliser :")
        label_mail_smtp.set_alignment(0,0)
        boite3_mail.pack_start(label_mail_smtp, False, False, 0)
        label_mail_smtp.show()
        # self.entry_mail_smtp
        self.entry_mail_smtp = gtk.Entry()
        self.entry_mail_smtp.set_text("smtp.orange.fr")
        boite3_mail.pack_start(self.entry_mail_smtp, False, False, 0)
        self.entry_mail_smtp.show()

        # label_mail_date
        label_mail_date = gtk.Label("Date (JJ-MM-AAAA hh:mm:ss) (facultative) :")
        label_mail_date.set_alignment(0,0)
        boite4_mail.pack_start(label_mail_date, False, False, 0)
        label_mail_date.show()
        # self.entry_mail_nb_env
        self.entry_mail_date = gtk.Entry()
        boite4_mail.pack_start(self.entry_mail_date, False, False, 0)
        self.entry_mail_date.show()

        # label_mail_from
        label_mail_from = gtk.Label("From :")
        label_mail_from.set_alignment(0,0)
        boite3_mail.pack_start(label_mail_from, False, False, 0)
        label_mail_from.show()

        # self.entry_mail_from
        self.entry_mail_from = gtk.Entry()
        boite3_mail.pack_start(self.entry_mail_from, False, False, 0)
        self.entry_mail_from.show()

        # label_mail_to
        label_mail_to = gtk.Label("To :")
        label_mail_to.set_alignment(0,0)
        boite4_mail.pack_start(label_mail_to, False, False, 0)
        label_mail_to.show()
        # self.entry_mail_to
        self.entry_mail_to = gtk.Entry()
        boite4_mail.pack_start(self.entry_mail_to, True, True, 0)
        self.entry_mail_to.show()

        # label_mail_sujet
        label_mail_sujet = gtk.Label("Sujet du mail (facultatif) :")
        label_mail_sujet.set_alignment(0,0)
        boite1_mail.pack_start(label_mail_sujet, False, False, 0)
        label_mail_sujet.show()
        # self.entry_mail_sujet
        self.entry_mail_sujet = gtk.Entry()
        boite1_mail.pack_start(self.entry_mail_sujet, False, False, 0)
        self.entry_mail_sujet.show()

        # label_mail_piece_j
        label_mail_piece_j = gtk.Label("Pièce jointe (facultative) :")
        label_mail_piece_j.set_alignment(0,0)
        boite1_mail.pack_start(label_mail_piece_j, False, False, 0)
        label_mail_piece_j.show()

        # boite5_mail
        boite5_mail = gtk.HBox(False, 5)
        boite1_mail.pack_start(boite5_mail, False, False, 0)
        boite5_mail.show()

        # self.entry_mail_piece_j
        self.entry_mail_piece_j = gtk.Entry()
        boite5_mail.pack_start(self.entry_mail_piece_j, True, True, 0)
        self.entry_mail_piece_j.show()

        # btn_mail_piece_j
        btn_mail_piece_j = gtk.Button("Ouvrir")
        btn_mail_piece_j.set_size_request(int(btn_mail_piece_j.size_request()[0]*1.1),btn_mail_piece_j.size_request()[1])
        boite5_mail.pack_start(btn_mail_piece_j, False, False, 0)
        btn_mail_piece_j.connect("clicked", self.dialogueOuvrirPieceJ)
        btn_mail_piece_j.show()

        # label_mail_corps
        label_mail_corps = gtk.Label("Corps du mail (facultatif) :")
        label_mail_corps.set_alignment(0,0)
        boite1_mail.pack_start(label_mail_corps, False, False, 0)
        label_mail_corps.show()
        # self.scrollbar_mail_corps
        scrolled_mail_corps = gtk.ScrolledWindow()
        boite1_mail.pack_start(scrolled_mail_corps, True, True, 0)
        scrolled_mail_corps.show()
        # self.textview_mail_corps
        self.textview_mail_corps = gtk.TextView()
        scrolled_mail_corps.add(self.textview_mail_corps)
        scrolled_mail_corps.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_mail_corps.show()

        # label_mail_nb_env
        label_mail_nb_env = gtk.Label("Nombre :")
        label_mail_nb_env.set_alignment(0,0)
        boite1_mail.pack_start(label_mail_nb_env, False, False, 0)
        label_mail_nb_env.show()

        # boite6_mail
        boite6_mail = gtk.HBox(False, 5)
        boite1_mail.pack_start(boite6_mail, False, False, 0)
        boite6_mail.show()

        # self.entry_mail_nb_env
        self.entry_mail_nb_env = gtk.Entry()
        self.entry_mail_nb_env.set_text("1")
        self.entry_mail_nb_env.set_size_request(75,self.entry_mail_nb_env.size_request()[1])
        boite6_mail.pack_start(self.entry_mail_nb_env, False, False, 0)
        self.entry_mail_nb_env.show()

        # self.progressbarMail
        self.progressbarMail = gtk.ProgressBar()
        boite6_mail.pack_start(self.progressbarMail, True, True, 0)
        self.progressbarMail.show()

        # self.btn_env_mail
        self.btn_env_mail = gtk.Button("Envoyer")
        self.btn_env_mail.set_size_request(int(self.btn_env_mail.size_request()[0]*1.1),self.btn_env_mail.size_request()[1])
        boite6_mail.pack_start(self.btn_env_mail, False, False, 0)
        self.btn_env_mail.connect("clicked", self.mkThreadMail)
        self.btn_env_mail.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_mail, gtk.Label("Mail \"Anonyme\""), -1)

    def tabASM(self): # TAB ASM
    # boites
        boite1_asm = gtk.VBox(False, 5)
        boite1_asm.show()
        boite2_asm = gtk.HBox(False, 5)
        boite1_asm.pack_start(boite2_asm, False, False, 0)
        boite2_asm.show()
        boite3_asm = gtk.VBox(False, 0)
        boite2_asm.pack_start(boite3_asm, True, True, 0)
        boite3_asm.show()
        boite4_asm = gtk.VBox(False, 0)
        boite2_asm.pack_start(boite4_asm, False, False, 0)
        boite4_asm.show()

        # label
        label_bin_asm = gtk.Label("Binaire :")
        label_bin_asm.set_alignment(0, 0)
        boite3_asm.pack_start(label_bin_asm, False, False, 0)
        label_bin_asm.show()

        # self.entry_bin_asm
        self.entry_bin_asm = gtk.Entry()
        boite3_asm.pack_start(self.entry_bin_asm, True, True, 5)
        self.entry_bin_asm.show()

        # label_desass_asm
        label_desass_asm = gtk.Label("Désassembler :")
        label_desass_asm.set_alignment(0, 0)
        boite3_asm.pack_start(label_desass_asm, False, False, 0)
        label_desass_asm.show()

        # self.entry_desass_asm
        self.entry_desass_asm = gtk.Entry()
        self.entry_desass_asm.set_text("main")
        boite3_asm.pack_start(self.entry_desass_asm, True, True, 5)
        self.entry_desass_asm.show()

        # btn_desass_asm
        btn_desass_asm = gtk.Button("ok")
        btn_desass_asm.set_size_request(int(btn_desass_asm.size_request()[0]),btn_desass_asm.size_request()[1])
        btn_desass_asm.connect("clicked", self.asm2human)
        boite4_asm.pack_end(btn_desass_asm, False, False, 4)
        btn_desass_asm.show()

        # btn_file_asm
        btn_file_asm = gtk.Button("Ouvrir")
        btn_file_asm.set_size_request(int(btn_file_asm.size_request()[0]*1.1),btn_file_asm.size_request()[1])
        btn_file_asm.connect("clicked", self.dialogueOuvrirBin)
        boite4_asm.pack_end(btn_file_asm, False, False, 20)
        btn_file_asm.show()

        # separateur_asm
        separateur_asm = gtk.HSeparator()
        boite1_asm.pack_start(separateur_asm, False, False, 0)
        separateur_asm.show()

        # label_sortie_asm
        label_sortie_asm = gtk.Label("Résultat :")
        label_sortie_asm.set_alignment(0,0)
        boite1_asm.pack_start(label_sortie_asm, False, False, 0)
        label_sortie_asm.show()

        # self.liststore_asm
        self.liststore_asm = gtk.ListStore(str, str, str, str)
        # scrollbar_sortie_asm
        scrolled_sortie_asm = gtk.ScrolledWindow()
        boite1_asm.pack_start(scrolled_sortie_asm, True, True, 0)
        scrolled_sortie_asm.show()
        # self.treeasview_sortie_asm
        treeview_sortie_asm = gtk.TreeView(self.liststore_asm)
        treeview_sortie_asm.set_rules_hint(True)
        treeview_sortie_asm.append_column(gtk.TreeViewColumn("Adresse", gtk.CellRendererText(), text=0))
        treeview_sortie_asm.append_column(gtk.TreeViewColumn("Position", gtk.CellRendererText(), text=1))
        treeview_sortie_asm.append_column(gtk.TreeViewColumn("Instruction", gtk.CellRendererText(), text=2))
        treeview_sortie_asm.append_column(gtk.TreeViewColumn("Traduction", gtk.CellRendererText(), text=3))
        scrolled_sortie_asm.add(treeview_sortie_asm)
        scrolled_sortie_asm.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        treeview_sortie_asm.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_asm, gtk.Label("Traducteur ASM"), -1)

    def tabARP(self): # TAB ARP
    # self.fixed_arp
        self.fixed_arp = gtk.Fixed()
        # self.label_bin
        self.label_arp = gtk.Label("ARP Poisoning")
        self.label_arp.set_alignment(0,0)
        self.label_arp.set_size_request(400,30)
        self.fixed_arp.put(self.label_arp, 25, 25)
        self.label_arp.show()

        # Affichage
        self.fixed_arp.show()
        self.bloc_tabs.insert_page(self.fixed_arp, gtk.Label("ARP-Poisoning"), -1)

    def tabCouchesRVB(self): # TAB Couches RVB
    # boites
        boite1_c_rgb = gtk.VBox(False, 5)
        boite1_c_rgb.show()
        boite2_c_rgb = gtk.HBox(False, 0)
        boite1_c_rgb.pack_start(boite2_c_rgb, False, False, 0)
        boite2_c_rgb.show()
        boite3_c_rgb = gtk.VBox(False, 5)
        boite2_c_rgb.pack_start(boite3_c_rgb, True, True, 0)
        boite3_c_rgb.show()
        boite4_c_rgb = gtk.VBox(False, 5)
        boite2_c_rgb.pack_start(boite4_c_rgb, True, True, 0)
        boite4_c_rgb.show()

        # label_choix_c_rgb
        label_choix_c_rgb = gtk.Label("Que faire ?")
        label_choix_c_rgb.set_alignment(0, 0)
        boite3_c_rgb.pack_start(label_choix_c_rgb, False, False, 0)
        label_choix_c_rgb.show()
        # self.btn_radio_hide_c_rgb, read
        self.btn_radio_hide_c_rgb = gtk.RadioButton(None, "Cacher un message dans une image")
        boite3_c_rgb.pack_start(self.btn_radio_hide_c_rgb, False, False, 0)
        self.btn_radio_hide_c_rgb.show()
        self.btn_radio_read_c_rgb = gtk.RadioButton(self.btn_radio_hide_c_rgb, "Lire un message caché dans une image")
        boite3_c_rgb.pack_start(self.btn_radio_read_c_rgb, False, False, 0)
        self.btn_radio_read_c_rgb.show()

        # On vide le champ résultat dès changement d'une option
        self.btn_radio_hide_c_rgb.connect("toggled", self.choixCouchesRVB)

        # self.label_choix_couche_rgb
        self.label_choix_couche_rgb = gtk.Label("Quelle couche utiliser ?")
        self.label_choix_couche_rgb.set_alignment(0, 0)
        boite4_c_rgb.pack_start(self.label_choix_couche_rgb, False, False, 0)
        self.label_choix_couche_rgb.show()

        # self.btn_radio_rouge_c_rgb, vert et bleu
        self.btn_radio_rouge_c_rgb = gtk.RadioButton(None, "rouge")
        boite4_c_rgb.pack_start(self.btn_radio_rouge_c_rgb, False, False, 0)
        self.btn_radio_rouge_c_rgb.show()
        self.btn_radio_vert_c_rgb = gtk.RadioButton(self.btn_radio_rouge_c_rgb, "vert")
        boite4_c_rgb.pack_start(self.btn_radio_vert_c_rgb, False, False, 0)
        self.btn_radio_vert_c_rgb.show()
        self.btn_radio_bleu_c_rgb = gtk.RadioButton(self.btn_radio_rouge_c_rgb, "bleu")
        boite4_c_rgb.pack_start(self.btn_radio_bleu_c_rgb, False, False, 0)
        self.btn_radio_bleu_c_rgb.show()

        # separateur_c_rgb
        separateur_c_rgb = gtk.HSeparator()
        boite1_c_rgb.pack_start(separateur_c_rgb, False, False, 0)
        separateur_c_rgb.show()

        # On vide les résultats dès changement d'une option
        self.btn_radio_rouge_c_rgb.connect("toggled", self.switchColor, 'r')
        self.btn_radio_vert_c_rgb.connect("toggled", self.switchColor, 'v')
        self.btn_radio_bleu_c_rgb.connect("toggled", self.switchColor, 'b')

        # self.boite_texte_c_rgb
        self.boite_texte_c_rgb = gtk.VBox(False, 5)
        boite1_c_rgb.pack_start(self.boite_texte_c_rgb, True, True, 0)
        self.boite_texte_c_rgb.show()
        # self.label_texte_c_rgb
        self.label_texte_c_rgb = gtk.Label("Texte :")
        self.label_texte_c_rgb.set_alignment(0,0)
        self.boite_texte_c_rgb.pack_start(self.label_texte_c_rgb, False, False, 0)
        self.label_texte_c_rgb.show()
        # scrollbar_entree
        self.scrolled_texte_c_rgb = gtk.ScrolledWindow()
        self.boite_texte_c_rgb.pack_start(self.scrolled_texte_c_rgb, True, True, 0) #####
        self.scrolled_texte_c_rgb.show()
        # self.textview_texte_c_rgb
        self.textview_texte_c_rgb = gtk.TextView()
        self.scrolled_texte_c_rgb.add(self.textview_texte_c_rgb)
        self.scrolled_texte_c_rgb.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_texte_c_rgb.show()

        # self.label_img_c_rgb
        self.label_img_c_rgb = gtk.Label("Fichier image :")
        self.label_img_c_rgb.set_alignment(0,0)
        boite1_c_rgb.pack_start(self.label_img_c_rgb, False, False, 0)
        self.label_img_c_rgb.show()
        # boite5_c_rgb
        boite5_c_rgb = gtk.HBox(False, 5)
        boite1_c_rgb.pack_start(boite5_c_rgb, False, False, 0)
        boite5_c_rgb.show()
        # self.entry_img_c_rgb
        self.entry_img_c_rgb = gtk.Entry()
        boite5_c_rgb.pack_start(self.entry_img_c_rgb, True, True, 0)
        self.entry_img_c_rgb.show()
        # self.btn_img_c_rgb
        self.btn_img_c_rgb = gtk.Button("Ouvrir")
        self.btn_img_c_rgb.set_size_request(int(self.btn_img_c_rgb.size_request()[0]*1.1),self.btn_img_c_rgb.size_request()[1])
        boite5_c_rgb.pack_start(self.btn_img_c_rgb, False, False, 0)
        self.btn_img_c_rgb.connect("clicked", self.dialogueFichierStega)
        self.btn_img_c_rgb.show()

        # self.boite_apercu_c_rgb
        self.boite_apercu_c_rgb = gtk.VBox(False, 0) # vbox d'aperçu des images
        boite1_c_rgb.pack_start(self.boite_apercu_c_rgb, True, True, 0)
        self.boite_apercu_c_rgb.show()
        # boite6_c_rgb
        boite6_c_rgb = gtk.HBox(False, 5) # vbox + vbox
        self.boite_apercu_c_rgb.pack_start(boite6_c_rgb, True, True, 0)
        boite6_c_rgb.show()
        # boite7_c_rgb
        boite7_c_rgb = gtk.VBox(False, 5) # label + txtview
        boite6_c_rgb.pack_start(boite7_c_rgb, True, True, 0)
        boite7_c_rgb.show()
        # self.boite8_c_rgb
        self.boite8_c_rgb = gtk.VBox(False, 5) # hbox + txtview
        boite6_c_rgb.pack_start(self.boite8_c_rgb, True, True, 0)
        self.boite8_c_rgb.show()
        # boite9_c_rgb
        boite9_c_rgb = gtk.HBox(False, 0) # label + btn enr
        self.boite8_c_rgb.pack_start(boite9_c_rgb, False, False, 0)
        boite9_c_rgb.show()

        # self.label_img_orig_c_rgb
        self.label_img_orig_c_rgb = gtk.Label("Image originale :")
        self.label_img_orig_c_rgb.set_alignment(0,0)
        boite7_c_rgb.pack_start(self.label_img_orig_c_rgb, False, False, 0)
        self.label_img_orig_c_rgb.show()
        # self.scrollbar_img_orig_c_rgb
        self.scrolled_img_orig_c_rgb = gtk.ScrolledWindow()
        boite7_c_rgb.pack_start(self.scrolled_img_orig_c_rgb, True, True, 0)
        self.scrolled_img_orig_c_rgb.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_img_orig_c_rgb.show()

        # self.label_img_result_c_rgb
        self.label_img_result_c_rgb = gtk.Label("Image finale :")
        self.label_img_result_c_rgb.set_alignment(0,0)
        boite9_c_rgb.pack_start(self.label_img_result_c_rgb, False, False, 0)
        self.label_img_result_c_rgb.show()
        # On crée une boîte à évènement pour le bouton engeristrer
        self.boite_evenement_enr_result_c_rgb = gtk.EventBox()
        self.boite_evenement_enr_result_c_rgb.set_visible_window(False)
        boite9_c_rgb.pack_end(self.boite_evenement_enr_result_c_rgb, False, False, 0)
        # self.image_enr_result_c_rgb
        self.image_enr_result_c_rgb = gtk.Image()
        self.image_enr_result_c_rgb.set_from_file("%s/images/enregistrer.png" % FKTB_PATH)
        self.boite_evenement_enr_result_c_rgb.add(self.image_enr_result_c_rgb)
        self.image_enr_result_c_rgb.show()
        # On relie une action à la boîte
        self.boite_evenement_enr_result_c_rgb.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.boite_evenement_enr_result_c_rgb.connect("button_press_event", self.enrResultCouchesRVB)
        self.boite_evenement_enr_result_c_rgb.show()
        # self.scrollbar_img_result
        self.scrolled_img_result_c_rgb = gtk.ScrolledWindow()
        self.boite8_c_rgb.pack_start(self.scrolled_img_result_c_rgb, True, True, 0)
        self.scrolled_img_result_c_rgb.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_img_result_c_rgb.show()

        # Affichage
        self.cleanCouchesRVB()
        self.scale = 1
        self.bloc_tabs.insert_page(boite1_c_rgb, gtk.Label("Couches RVB"), -1)

    def tabOpNot(self): # TAB Opérateur NOT
    # boites
        boite1_op_not = gtk.VBox(False, 5)
        boite1_op_not.show()

        # self.label_in_file_op_not
        self.label_in_file_op_not = gtk.Label("Fichier d'entrée :")
        self.label_in_file_op_not.set_alignment(0, 0)
        boite1_op_not.pack_start(self.label_in_file_op_not, False, False, 0)
        self.label_in_file_op_not.show()

        # boite2_op_not
        boite2_op_not = gtk.HBox(False, 5)
        boite1_op_not.pack_start(boite2_op_not, False, False, 0)
        boite2_op_not.show()
        # self.entry_in_file_op_not
        self.entry_in_file_op_not = gtk.Entry()
        boite2_op_not.pack_start(self.entry_in_file_op_not, True, True, 0)
        self.entry_in_file_op_not.show()
        # self.btn_img_op_not
        self.btn_img_op_not = gtk.Button("Ouvrir")
        self.btn_img_op_not.set_size_request(int(self.btn_img_op_not.size_request()[0]*1.1),self.btn_img_op_not.size_request()[1])
        boite2_op_not.pack_start(self.btn_img_op_not, False, False, 0)
        self.btn_img_op_not.connect("clicked", self.dialogueOuvrirOpNot)
        self.btn_img_op_not.show()

        # self.label_out_file_op_not
        self.label_out_file_op_not = gtk.Label("Sortie :")
        self.label_out_file_op_not.set_alignment(0, 0)
        boite1_op_not.pack_start(self.label_out_file_op_not, False, False, 0)
        self.label_out_file_op_not.show()

        # boite3_op_not
        boite3_op_not = gtk.HBox(False, 5)
        boite1_op_not.pack_start(boite3_op_not, False, False, 0)
        boite3_op_not.show()

        # self.progressbarOpNot
        self.progressbarOpNot = gtk.ProgressBar()
        boite3_op_not.pack_start(self.progressbarOpNot, True, True, 0)
        self.progressbarOpNot.show()

        # self.btn_save_out_op_not
        self.btn_save_out_op_not = gtk.Button("Enregistrer")
        self.btn_save_out_op_not.set_sensitive(False)
        self.btn_save_out_op_not.set_size_request(int(self.btn_save_out_op_not.size_request()[0]*1.1),self.btn_save_out_op_not.size_request()[1])
        self.btn_save_out_op_not.connect("clicked", self.saveOutOpNot)
        boite3_op_not.pack_start(self.btn_save_out_op_not, False, False, 0)
        self.btn_save_out_op_not.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_op_not, gtk.Label("Opérateur NOT"), -1)

    def tabXOR(self): # TAB XOR
    # boites
        boite1_xor = gtk.VBox(False, 5)
        boite1_xor.show()
        boite2_xor = gtk.HBox(False, 5)
        boite1_xor.pack_start(boite2_xor, False, False, 0)
        boite2_xor.show()
        boite3_xor = gtk.VBox(False, 0)
        boite2_xor.pack_start(boite3_xor, True, True, 0)
        boite3_xor.show()
        boite4_xor = gtk.VBox(False, 0)
        boite2_xor.pack_start(boite4_xor, False, False, 0)
        boite4_xor.show()

        # label_key_xor
        label_key_xor = gtk.Label("Clé utilisée :")
        label_key_xor.set_alignment(0, 0)
        boite3_xor.pack_start(label_key_xor, False, False, 0)
        label_key_xor.show()

        # self.entry_key_xor
        self.entry_key_xor = gtk.Entry()
        self.entry_key_xor.set_text("xor")
        boite3_xor.pack_start(self.entry_key_xor, True, True, 5)
        self.entry_key_xor.show()

        # btn_chiffrer_xor
        btn_chiffrer_xor = gtk.Button("ok")
        btn_chiffrer_xor.set_size_request(int(btn_chiffrer_xor.size_request()[0]*1.2),btn_chiffrer_xor.size_request()[1])
        btn_chiffrer_xor.connect("clicked", self.xor)
        boite4_xor.pack_end(btn_chiffrer_xor, False, False, 4)
        btn_chiffrer_xor.show()

        # separateur_xor
        separateur_xor = gtk.HSeparator()
        boite1_xor.pack_start(separateur_xor, False, False, 0)
        separateur_xor.show()

        # boite2_xor
        boite5_xor = gtk.HBox(False, 5)
        boite1_xor.pack_start(boite5_xor, False, False, 0)
        boite5_xor.show()

        # label_entree_xor
        label_entree_xor = gtk.Label("Texte à chiffrer / déchiffrer :")
        label_entree_xor.set_alignment(0,1)
        boite5_xor.pack_start(label_entree_xor, False, False, 0)
        label_entree_xor.show()

        # self.combo_entree_xor
        self.combo_entree_xor = gtk.combo_box_new_text()
        self.combo_entree_xor.append_text("ASCII")
        self.combo_entree_xor.append_text("Décimal")
        self.combo_entree_xor.set_active(0)
        boite5_xor.pack_end(self.combo_entree_xor, False, False, 0)
        self.combo_entree_xor.show()

        # scrollbar_entree_xor
        scrolled_entree_xor = gtk.ScrolledWindow()
        boite1_xor.pack_start(scrolled_entree_xor, True, True, 0)
        scrolled_entree_xor.show()
        # self.textview_entree_xor
        self.textview_entree_xor = gtk.TextView()
        scrolled_entree_xor.add(self.textview_entree_xor)
        scrolled_entree_xor.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_entree_xor.show()

        # boite6_xor
        boite6_xor = gtk.HBox(False, 5)
        boite1_xor.pack_start(boite6_xor, False, False, 0)
        boite6_xor.show()

        # label_sortie_xor
        label_sortie_xor = gtk.Label("Résultat :")
        label_sortie_xor.set_alignment(0,1)
        boite6_xor.pack_start(label_sortie_xor, False, False, 0)
        label_sortie_xor.show()

        # self.combo_sortie_xor
        self.combo_sortie_xor = gtk.combo_box_new_text()
        self.combo_sortie_xor.append_text("ASCII")
        self.combo_sortie_xor.append_text("Décimal")
        self.combo_sortie_xor.set_active(0)
        boite6_xor.pack_end(self.combo_sortie_xor, False, False, 0)
        self.combo_sortie_xor.show()
        # scrollbar_sortie_xor
        scrolled_sortie_xor = gtk.ScrolledWindow()
        boite1_xor.pack_start(scrolled_sortie_xor, True, True, 0)
        scrolled_sortie_xor.show()
        # self.textview_sortie_xor
        self.textview_sortie_xor = gtk.TextView()
        self.textview_sortie_xor.set_editable(False)
        scrolled_sortie_xor.add(self.textview_sortie_xor)
        scrolled_sortie_xor.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_sortie_xor.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_xor, gtk.Label("Chiffrement XOR"), -1)

    def tabVigenere(self): # TAB Vigenere
    # boites
        boite1_vigenere = gtk.VBox(False, 5)
        boite1_vigenere.show()
        boite2_vigenere = gtk.HBox(False, 5)
        boite1_vigenere.pack_start(boite2_vigenere, False, False, 0)
        boite2_vigenere.show()
        boite3_vigenere = gtk.VBox(False, 0)
        boite2_vigenere.pack_start(boite3_vigenere, True, True, 0)
        boite3_vigenere.show()
        boite4_vigenere = gtk.VBox(False, 0)
        boite2_vigenere.pack_start(boite4_vigenere, False, False, 0)
        boite4_vigenere.show()
        boite5_vigenere = gtk.VBox(False, 0)
        boite2_vigenere.pack_start(boite5_vigenere, False, False, 0)
        boite5_vigenere.show()

        # label_key_vigenere
        label_key_vigenere = gtk.Label("Clé utilisée :")
        label_key_vigenere.set_alignment(0, 0)
        boite3_vigenere.pack_start(label_key_vigenere, False, False, 0)
        label_key_vigenere.show()

        # self.entry_key_vigenere
        self.entry_key_vigenere = gtk.Entry()
        self.entry_key_vigenere.set_text("VIGENERE")
        boite3_vigenere.pack_start(self.entry_key_vigenere, True, True, 5)
        self.entry_key_vigenere.show()

        # btn_chiffrer_vigenere
        btn_chiffrer_vigenere = gtk.Button("Chiffrer")
        btn_chiffrer_vigenere.set_size_request(int(btn_chiffrer_vigenere.size_request()[0]*1.1),btn_chiffrer_vigenere.size_request()[1])
        btn_chiffrer_vigenere.connect("clicked", self.vigenere, 1)
        boite4_vigenere.pack_end(btn_chiffrer_vigenere, False, False, 4)
        btn_chiffrer_vigenere.show()

        # btn_dechiffrer_vigenere
        btn_dechiffrer_vigenere = gtk.Button("Déchiffrer")
        btn_dechiffrer_vigenere.set_size_request(int(btn_dechiffrer_vigenere.size_request()[0]*1.1),btn_dechiffrer_vigenere.size_request()[1])
        btn_dechiffrer_vigenere.connect("clicked", self.vigenere, 0)
        boite5_vigenere.pack_end(btn_dechiffrer_vigenere, False, False, 4)
        btn_dechiffrer_vigenere.show()

        # separateur_vigenere
        separateur_vigenere = gtk.HSeparator()
        boite1_vigenere.pack_start(separateur_vigenere, False, False, 0)
        separateur_vigenere.show()

        # label_entree_vigenere
        label_entree_vigenere = gtk.Label("Texte à chiffrer / déchiffrer :")
        label_entree_vigenere.set_alignment(0,0)
        boite1_vigenere.pack_start(label_entree_vigenere, False, False, 0)
        label_entree_vigenere.show()
        # scrollbar_entree_vigenere
        scrolled_entree_vigenere = gtk.ScrolledWindow()
        boite1_vigenere.pack_start(scrolled_entree_vigenere, True, True, 0)
        scrolled_entree_vigenere.show()
        # self.textview_entree_vigenere
        self.textview_entree_vigenere = gtk.TextView()
        scrolled_entree_vigenere.add(self.textview_entree_vigenere)
        scrolled_entree_vigenere.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_entree_vigenere.show()

        # label_sortie_vigenere
        label_sortie_vigenere = gtk.Label("Résultat :")
        label_sortie_vigenere.set_alignment(0,0)
        boite1_vigenere.pack_start(label_sortie_vigenere, False, False, 0)
        label_sortie_vigenere.show()
        # scrollbar_sortie_vigenere
        scrolled_sortie_vigenere = gtk.ScrolledWindow()
        boite1_vigenere.pack_start(scrolled_sortie_vigenere, True, True, 0)
        scrolled_sortie_vigenere.show()
        # self.textview_sortie_vigenere
        self.textview_sortie_vigenere = gtk.TextView()
        self.textview_sortie_vigenere.set_editable(False)
        scrolled_sortie_vigenere.add(self.textview_sortie_vigenere)
        scrolled_sortie_vigenere.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_sortie_vigenere.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_vigenere, gtk.Label("Chiffre de Vigenère"), -1)

    def tabConvASCII(self): # TAB Conversion de base
    # boites
        boite1_conv = gtk.VBox(False, 5)
        boite1_conv.show()

        ###

        # label_in_type_conv
        label_in_type_conv = gtk.Label("Entrée :")
        label_in_type_conv.set_alignment(0,0)
        boite1_conv.pack_start(label_in_type_conv, False, False, 0)
        label_in_type_conv.show()
        # scrollbar_in_type_conv
        scrolled_in_type_conv = gtk.ScrolledWindow()
        boite1_conv.pack_start(scrolled_in_type_conv, True, True, 0)
        scrolled_in_type_conv.show()
        # self.textview_in_conv
        self.textview_in_conv = gtk.TextView()
        scrolled_in_type_conv.add(self.textview_in_conv)
        scrolled_in_type_conv.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_in_conv.show()

        ###

        # label_out_type_conv
        label_out_type_conv = gtk.Label("Sortie :")
        label_out_type_conv.set_alignment(0,0)
        boite1_conv.pack_start(label_out_type_conv, False, False, 0)
        label_out_type_conv.show()
        # scrollbar_out_type_conv
        scrolled_out_type_conv = gtk.ScrolledWindow()
        boite1_conv.pack_start(scrolled_out_type_conv, True, True, 0)
        scrolled_out_type_conv.show()
        # self.textview_out_conv
        self.textview_out_conv = gtk.TextView()
        scrolled_out_type_conv.add(self.textview_out_conv)
        scrolled_out_type_conv.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_out_conv.set_editable(False)
        self.textview_out_conv.show()

        # separateur_conv
        separateur_conv = gtk.HSeparator()
        boite1_conv.pack_start(separateur_conv, False, False, 5)
        separateur_conv.show()

        # boite2_conv
        boite2_conv = gtk.HBox(False, 5)
        boite1_conv.pack_start(boite2_conv, False, False, 0)
        boite2_conv.show()

        # self.combo_conv
        self.combo_conv = gtk.combo_box_new_text()
        self.combo_conv.append_text("ASCII")
        self.combo_conv.append_text("Hexadécimal")
        self.combo_conv.append_text("Décimal")
        self.combo_conv.append_text("Octal")
        self.combo_conv.append_text("Binaire")
        self.combo_conv.set_active(0)
        boite2_conv.pack_start(self.combo_conv, False, False, 0)
        self.combo_conv.show()

        # label_to_conv
        label_to_conv = gtk.Label(">")
        label_to_conv.set_alignment(0,0.5)
        boite2_conv.pack_start(label_to_conv, False, False, 0)
        label_to_conv.show()

        # self.combo_conv2
        self.combo_conv2 = gtk.combo_box_new_text()
        self.combo_conv2.append_text("ASCII")
        self.combo_conv2.append_text("Hexadécimal")
        self.combo_conv2.append_text("Décimal")
        self.combo_conv2.append_text("Octal")
        self.combo_conv2.append_text("Binaire")
        self.combo_conv2.set_active(1)
        boite2_conv.pack_start(self.combo_conv2, False, False, 0)
        self.combo_conv2.show()

        # btn_conv
        btn_conv = gtk.Button("Convertir")
        btn_conv.set_size_request(int(btn_conv.size_request()[0]*1.1),btn_conv.size_request()[1])
        btn_conv.connect("clicked", self.convASCII)
        boite2_conv.pack_start(btn_conv, False, False, 0)
        btn_conv.show()

        # btn_clean_conv
        btn_clean_conv = gtk.Button("Vider")
        btn_clean_conv.set_size_request(int(btn_clean_conv.size_request()[0]*1.1),btn_clean_conv.size_request()[1])
        btn_clean_conv.connect("clicked", self.cleanConv)
        boite2_conv.pack_end(btn_clean_conv, False, False, 0)
        btn_clean_conv.show()

        # btn_invert_conv
        btn_invert_conv = gtk.Button("Intervertir")
        btn_invert_conv.set_size_request(int(btn_invert_conv.size_request()[0]*1.1),btn_invert_conv.size_request()[1])
        btn_invert_conv.connect("clicked", self.invertConv)
        boite2_conv.pack_end(btn_invert_conv, False, False, 0)
        btn_invert_conv.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_conv, gtk.Label("Conversion de base"), -1)

    def cleanConv(self, parent=''):
        if parent != '':
            # Buffer, début et fin de buffer d'entrée
            txtbuf_in_conv = self.textview_in_conv.get_buffer()
            start_iter_in_conv = txtbuf_in_conv.get_start_iter()
            end_iter_in_conv = txtbuf_in_conv.get_end_iter()

            # Suppression du texte d'entrée
            txtbuf_in_conv.delete(start_iter_in_conv, end_iter_in_conv)

        # Buffer, début et fin de buffer de sortie
        txtbuf_out_conv = self.textview_out_conv.get_buffer()
        start_iter_out_conv = txtbuf_out_conv.get_start_iter()
        end_iter_out_conv = txtbuf_out_conv.get_end_iter()

        # Suppression de la sortie
        txtbuf_out_conv.delete(start_iter_out_conv, end_iter_out_conv)

    def invertConv(self, parent):
        txtbuf_in_conv = self.textview_in_conv.get_buffer()    # Buffer d'entrée
        txtbuf_out_conv = self.textview_out_conv.get_buffer()    # Buffer de sortie

        self.textview_in_conv.set_buffer(txtbuf_out_conv)    # Intervertion des buffer
        self.textview_out_conv.set_buffer(txtbuf_in_conv)

        in_type_conv = self.combo_conv.get_active()        # Élément séléctionné dans la combobox d'entrée
        out_type_conv = self.combo_conv2.get_active()        # Élément séléctionné dans la combobox de sortie

        self.combo_conv.set_active(out_type_conv)        # Intervertion des éléments des combobox
        self.combo_conv2.set_active(in_type_conv)

    def convASCII(self, parent):
        self.cleanConv()

        # Buffer et texte d'entrée
        txtbuf_in_conv = self.textview_in_conv.get_buffer()
        txt_in_conv = txtbuf_in_conv.get_text(txtbuf_in_conv.get_start_iter(),txtbuf_in_conv.get_end_iter())

        if not txt_in_conv: self.warnDialog('Veuillez renseigner le champ :\n\n\tEntrée')
        else:

            # Buffer, début et fin de buffer de sortie
            txtbuf_out_conv = self.textview_out_conv.get_buffer()
            start_iter_out_conv = txtbuf_out_conv.get_start_iter()

            in_type_conv = self.combo_conv.get_active()
            out_type_conv = self.combo_conv2.get_active()
            # 0 ascii
            # 1 hexadécimal
            # 2 décimal
            # 3 octal
            # 4 binaire

            problem=0
            if in_type_conv == 1: # HEXADÉCIMAL > ASCII
                txt_in_conv=re.sub('[\s]+', '', txt_in_conv)                 # Enlever tout les caractères d'espacement
                if re.compile("[^\da-fA-F]+", re.MULTILINE).search(txt_in_conv):
                    self.warnDialog("Erreur de saisie !\n\nUne code héxadécimal ne peux contenir que les caractères :\n0-9, a-f et A-F...")
                    problem=1
                elif len(txt_in_conv)%2 != 0:
                    self.warnDialog("Erreur de saisie !\n\nUn code hexadécimal est forcément d’une longueur égale à un multiple de 2...")
                    problem=1
                else: txt_in_conv=''.join(chr(int('0x'+i,16)) for i in [txt_in_conv[i*2:i*2+2] for i in range(len(txt_in_conv) / 2)])

            elif in_type_conv == 2: # DÉCIMAL > ASCII
                txt_in_conv=re.sub('[\s]+', ' ', txt_in_conv)                # Remplacer tout les caractères d'espacement par des espaces
                txt_in_conv=re.sub('[ ]+', ' ', txt_in_conv)                # Enlever les espaces multiples
                txt_in_conv=re.sub('^[ ]+', '', re.sub('[ ]+$', '', txt_in_conv))    # Enlever les espaces en début et fin de chaine
                if re.compile("[^ \d]+", re.MULTILINE).search(txt_in_conv):
                    self.warnDialog("Erreur de saisie !\n\nUne code décimal ne peux contenir que des chiffres...")
                    problem=1
                elif int(max(txt_in_conv.split(' '))) > 255:
                    self.warnDialog("Erreur de saisie !\n\nUne valeur décimale ne peux pas dépasser 255...")
                    problem=1
                else: txt_in_conv=''.join(chr(int(i)) for i in txt_in_conv.split(' '))

            elif in_type_conv == 3: # OCTAL > ASCII
                txt_in_conv=re.sub('[\s]+', ' ', txt_in_conv)                # Remplacer tout les caractères d'espacement par des espaces
                txt_in_conv=re.sub('[ ]+', ' ', txt_in_conv)                # Enlever les espaces multiples
                txt_in_conv=re.sub('^[ ]+', '', re.sub('[ ]+$', '', txt_in_conv))    # Enlever les espaces en début et fin de chaine
                if re.compile("[^ \d]+", re.MULTILINE).search(txt_in_conv):
                    self.warnDialog("Erreur de saisie !\n\nUne code octal ne peux contenir que des chiffres...")
                    problem=1
                elif int(max(txt_in_conv.split(' '))) > 377:
                    self.warnDialog("Erreur de saisie !\n\nUne valeur octale ne peux pas dépasser 377...")
                    problem=1
                else: txt_in_conv=''.join([chr(int(i,8)) for i in txt_in_conv.split(' ')])

            elif in_type_conv == 4: # BINAIRE > ASCII
                txt_in_conv=re.sub('[\s]+', '', txt_in_conv)                # Enlever tout les caractères d'espacement
                if re.compile("[^ 01]+", re.MULTILINE).search(txt_in_conv):
                    self.warnDialog("Erreur de saisie !\n\nUne code bianire ne peux contenir que les chiffres 0 et 1...")
                    problem=1
                elif len(txt_in_conv)%8 != 0:
                    self.warnDialog("Erreur de saisie !\n\nUn code binaire est forcément d’une longueur égale à un multiple de 8...")
                    problem=1
                else: txt_in_conv=''.join(chr(int(i,2)) for i in [txt_in_conv[i*8:i*8+8] for i in range(len(txt_in_conv) / 8)])

            if not problem:
                if out_type_conv == 0: # ASCII
                    try: txt_in_conv.decode('utf-8')
                    except UnicodeDecodeError: self.warnDialog("Affichage en ASCII impossible !\n\nLe code contient sûrement des caractères non imprimables...")
                    else:
                        if '\0' in txt_in_conv: self.warnDialog("Affichage en ASCII impossible !\n\nLe code contient sûrement des caractères non imprimables...")
                        else: txtbuf_out_conv.insert(start_iter_out_conv, txt_in_conv)

                elif out_type_conv == 1: # ASCII > HEXADÉCIMAL
                    txtbuf_out_conv.insert(start_iter_out_conv, ' '.join('0'+i if len(i)<2 else i for i in [hex(ord(i))[2:] for i in txt_in_conv]))
                elif out_type_conv == 2: # ASCII > DÉCIMAL
                    txtbuf_out_conv.insert(start_iter_out_conv, ' '.join(str(ord(i)) for i in txt_in_conv))
                elif out_type_conv == 3: # ASCII > OCTAL
                    txtbuf_out_conv.insert(start_iter_out_conv, ' '.join('0' if not i else i for i in [oct(ord(i)).lstrip('0') for i in txt_in_conv]))
                elif out_type_conv == 4: # ASCII > BINAIRE
                    txtbuf_out_conv.insert(start_iter_out_conv, ' '.join('0'*(8-len(i))+i for i in [bin(ord(i)).replace('0b','') for i in txt_in_conv]))

    def lastModif(self):
        self.treestore_lastmodif.clear()

        self.label_sortie_lastmodif.set_text("En cours ...")
        self.btn_lastmodif.set_sensitive(False)

        problem=0
        for char in ["|", "&", "`", ">", "<", "\""]:
            if char in self.entry_loc_lastmodif.get_text(): problem+=1
            if char in self.entry_excl_lastmodif.get_text(): problem+=1
            if char in self.entry_min_lastmodif.get_text(): problem+=1

        if not problem :
            find_time=strftime('%H:%M:%S et ', localtime(mktime(localtime())-int(self.entry_min_lastmodif.get_text())*60))+strftime('%H:%M:%S', localtime())

            cmd="find '"+self.entry_loc_lastmodif.get_text()+"' -type f "
            if len(self.entry_excl_lastmodif.get_text()): cmd+=''.join("-not -path '"+x+"' " for x in re.sub('^[\s]+', '', re.sub('[\s]+$', '',re.sub('[\s]+,[\s]+', ',', self.entry_excl_lastmodif.get_text()))).split(','))
            cmd+="-mmin -"+self.entry_min_lastmodif.get_text()

            # Vérification des permissions
            for su_gui_cmd in ['gksu','kdesu','ktsuss','beesu','']:
                if getoutput("which "+su_gui_cmd): break
            if not su_gui_cmd:
                gtk.gdk.threads_enter()
                self.msgbox("Un des outils suivant est nécessaire pour acquérir les droits administrateur, veuillez en installer un :\n\ngksu\nkdesu\nktsuss\nbeesu",1)
                gtk.gdk.threads_leave()
            else: self.findProcess=subprocess.Popen((su_gui_cmd,cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            bakTreeIter={}
            self.nbModified=0
            while 1:
                out=self.findProcess.stdout.readline().rstrip('\n')
                if not out and self.findProcess.poll() != None: break
                if out and not "find:" in out:
                    parent=None
                    for i in range(1,len(out.lstrip('/').split('/'))+1):
                        if i != len(out.lstrip('/').split('/')):
                        # dossier
                            if '/'+'/'.join(out.lstrip('/').split('/')[0:i]) in bakTreeIter.keys():
                                parent=bakTreeIter['/'+'/'.join(out.lstrip('/').split('/')[0:i])]
                            else:
                                parent=self.treestore_lastmodif.append(parent, [out.lstrip('/').split('/')[i-1]])
                                bakTreeIter['/'+'/'.join(out.lstrip('/').split('/')[0:i])]=parent
                        else:
                        # fichier
                            parent=self.treestore_lastmodif.append(parent, [out.lstrip('/').split('/')[i-1]])
                            self.nbModified+=1
                        i+=1

            self.label_sortie_lastmodif.set_text(str(self.nbModified)+" fichiers modifiés entre "+find_time+" :")
            self.btn_lastmodif.set_sensitive(True)
        else:
            self.label_sortie_lastmodif.set_text("Erreur de saisie !")
            self.btn_lastmodif.set_sensitive(True)

    def tabLastModif(self): # TAB last modif
    # boites
        boite1_lastmodif = gtk.VBox(False, 5)
        boite1_lastmodif.show()
        boite2_lastmodif = gtk.HBox(False, 5)
        boite1_lastmodif.pack_start(boite2_lastmodif, False, False, 0)
        boite2_lastmodif.show()
        boite3_lastmodif = gtk.VBox(False, 5)
        boite2_lastmodif.pack_start(boite3_lastmodif, True, True, 0)
        boite3_lastmodif.show()
        boite4_lastmodif = gtk.VBox(False, 5)
        boite2_lastmodif.pack_start(boite4_lastmodif, True, True, 0)
        boite4_lastmodif.show()

        # label_lastmodif_loc
        label_lastmodif_loc = gtk.Label("Emplacement :")
        label_lastmodif_loc.set_alignment(0,0)
        boite3_lastmodif.pack_start(label_lastmodif_loc, False, False, 0)
        label_lastmodif_loc.show()
        # self.entry_loc_lastmodif
        self.entry_loc_lastmodif = gtk.Entry()
        self.entry_loc_lastmodif.set_text("/")
        boite3_lastmodif.pack_start(self.entry_loc_lastmodif, False, False, 0)
        self.entry_loc_lastmodif.show()

        # label_lastmodif_min
        label_lastmodif_min = gtk.Label("Minutes :")
        label_lastmodif_min.set_alignment(0,0)
        boite4_lastmodif.pack_start(label_lastmodif_min, False, False, 0)
        label_lastmodif_min.show()
        # self.entry_lastmodif_nb_env
        self.entry_min_lastmodif = gtk.Entry()
        self.entry_min_lastmodif.set_text("1")
        boite4_lastmodif.pack_start(self.entry_min_lastmodif, False, False, 0)
        self.entry_min_lastmodif.show()

        # boites
        boite5_lastmodif = gtk.HBox(False, 5)
        boite1_lastmodif.pack_start(boite5_lastmodif, False, False, 0)
        boite5_lastmodif.show()
        boite6_lastmodif = gtk.VBox(False, 0)
        boite5_lastmodif.pack_start(boite6_lastmodif, True, True, 0)
        boite6_lastmodif.show()
        boite7_lastmodif = gtk.VBox(False, 0)
        boite5_lastmodif.pack_start(boite7_lastmodif, False, False, 0)
        boite7_lastmodif.show()

        # label_excl_lastmodif
        label_excl_lastmodif = gtk.Label("Exclure (séparer les éléments par une virgule) :")
        label_excl_lastmodif.set_alignment(0, 0)
        boite6_lastmodif.pack_start(label_excl_lastmodif, False, False, 0)
        label_excl_lastmodif.show()

        # self.entry_excl_lastmodif
        self.entry_excl_lastmodif = gtk.Entry()
        self.entry_excl_lastmodif.set_text("/sys*,/dev*,/proc*")
        boite6_lastmodif.pack_start(self.entry_excl_lastmodif, True, True, 5)
        self.entry_excl_lastmodif.show()

        # self.btn_lastmodif
        self.btn_lastmodif = gtk.Button("Check")
        self.btn_lastmodif.set_size_request(int(self.btn_lastmodif.size_request()[0]),self.btn_lastmodif.size_request()[1])
        self.btn_lastmodif.connect("clicked", lambda e: thread.start_new_thread(self.lastModif, ()))
        boite7_lastmodif.pack_end(self.btn_lastmodif, False, False, 4)
        self.btn_lastmodif.show()

        # separateur_lastmodif
        separateur_lastmodif = gtk.HSeparator()
        boite1_lastmodif.pack_start(separateur_lastmodif, False, False, 0)
        separateur_lastmodif.show()

        # self.label_sortie_lastmodif
        self.label_sortie_lastmodif = gtk.Label("En attente ...")
        self.label_sortie_lastmodif.set_alignment(0,0)
        boite1_lastmodif.pack_start(self.label_sortie_lastmodif, False, False, 0)
        self.label_sortie_lastmodif.show()

        # self.liststore_lastmodif
        self.liststore_lastmodif = gtk.ListStore(str, str, str, str)
        # scrollbar_sortie_lastmodif
        scrolled_sortie_lastmodif = gtk.ScrolledWindow()
        boite1_lastmodif.pack_start(scrolled_sortie_lastmodif, True, True, 0)
        scrolled_sortie_lastmodif.show()

        # self.treeview_lastmodif
        self.treeview_lastmodif = gtk.TreeView()
        self.column_lastmodif = gtk.TreeViewColumn()
        #        self.column_lastmodif.set_title("En attente ...")
        cell = gtk.CellRendererText()
        self.column_lastmodif.pack_start(cell, True)
        self.column_lastmodif.add_attribute(cell, "text", 0)
        self.treestore_lastmodif = gtk.TreeStore(str)
        self.treeview_lastmodif.append_column(self.column_lastmodif)
        self.treeview_lastmodif.set_headers_visible(False)
        self.treeview_lastmodif.set_model(self.treestore_lastmodif)
        scrolled_sortie_lastmodif.add(self.treeview_lastmodif)
        scrolled_sortie_lastmodif.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.treeview_lastmodif.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_lastmodif, gtk.Label("Moniteur de fichier"), -1)

    def hostname(self):
        self.liststore_hostname.clear()
        self.progressbarHostname.set_fraction(0)

        # Test avec l'interface eth0 (voir pour liste déroulante avec les interfaces)

        netInfo=self.ifaceInfo()
        if not netInfo:
            gtk.gdk.threads_enter()
            self.msgbox("Vous n'avez pas l'air connecté !",1) # Message à modifier
            gtk.gdk.threads_leave()
        else:
            netInfo=netInfo['eth0']
            print 'netInfo = '+str(netInfo)

            # ipAddr = netInfo[0] # '192.168.1.1'
            # networkAddr = netInfo[1] # '192.168.1.0'
            # broadcastAddr = netInfo[2] # '192.168.1.255'

            if not getoutput("which host"):
                os_info=getoutput("uname -a").lower()
                alert="Un outils est nécessaire, veuillez l'installer :\nhost - DNS lookup utility"
                alert+=''.join(["\n\n# apt-get install host\n(à vérifier)" for os in "backtrack","debian","ubuntu","mint","voyager" if os in os_info and not "apt-get" in alert])
                alert+=''.join(["\n\n# yum install host\n(à vérifier)" for os in "fedora","centos" if os in os_info and not "yum" in alert])
                gtk.gdk.threads_enter()
                self.msgbox(alert,1)
                gtk.gdk.threads_leave()
            elif not netInfo[1] in getoutput("route"):
                gtk.gdk.threads_enter()
                self.msgbox("La table de routage IP du noyau ne semble pas contenir de routes statiques vers le réseau ciblé !",1)
                gtk.gdk.threads_leave()
            else:
                self.btn_hostname.set_sensitive(False)

                #netAddr='192.160.0.0'
                #broadcastAddr='192.191.255.255'

                #firstAddr='.'.join(netAddr.split('.')[:3])+'.'+str(int(netAddr.split('.')[3])+1)
                #lastAddr='.'.join(broadcastAddr.split('.')[:3])+'.'+str(int(broadcastAddr.split('.')[3])-1)

                #print firstAddr,lastAddr

                #rangeIp=[]
                #for a in range(int(netAddr.split('.')[0]),int(broadcastAddr.split('.')[0])+1):
                #    for b in range(int(netAddr.split('.')[1]),int(broadcastAddr.split('.')[1])+1):
                #        for c in range(int(netAddr.split('.')[2]),int(broadcastAddr.split('.')[2])+1):
                #            for d in range(int(netAddr.split('.')[3]),int(broadcastAddr.split('.')[3])+1):
                #                rangeIp.append('.'.join((str(a),str(b),str(c),str(d))))

                #rangeIp=rangeIp[1:len(rangeIp)-1] # virer les adresses : du réseau et de broadcast

                #192.160.0.0 => 192.191.255.255
                #192.160.0.1 => 192.191.255.254 (256*256-2 = 65534 possibilités)
                #102.0.0.1 => 102.255.255.254 (256*256*256-2 = 16777214 possibilités)
                #utiliser le for pour les dns qry et if ifserv ou ipbroadcast zapper

                iMin=int(netInfo[1].split('.')[3])+1
                iMax=int(netInfo[2].split('.')[3])-1
                print 'iMin = '+str(iMin)
                print 'iMax = '+str(iMax)
                i=iMin
                while i <= iMax:
                    ip='.'.join(netInfo[1].split('.')[:3])+'.' +str(i)
                    #print 'ip = '+ip
                    res=getoutput("host -W 5 "+ip+" | grep -v 'not found' | awk '{print $NF}' | awk 'sub(\".$\",\"\")'")
                    if res: self.liststore_hostname.append((ip, res))
                    #else:print ip+' '*(15-len(Ip))+"not found"
                    self.progressbarHostname.set_fraction(i/float(iMax))
                    self.progressbarHostname.set_text("Recherche en cours ("+str(i)+"/"+str(iMax)+")")
                    i+=1

                self.progressbarHostname.set_text("Recherche terminée ("+strftime('%H:%M:%S', localtime())+")")
                self.btn_hostname.set_sensitive(True)

    def tabHostname(self): # TAB Hostname Lookup
    # boites
        boite1_hostname = gtk.VBox(False, 5)
        boite1_hostname.show()

        # self.liststore_hostname
        self.liststore_hostname = gtk.ListStore(str, str)
        # scrollbar_sortie_hostname
        scrolled_sortie_hostname = gtk.ScrolledWindow()
        boite1_hostname.pack_start(scrolled_sortie_hostname, True, True, 0)
        scrolled_sortie_hostname.show()
        # self.treeview_sortie_hostname
        treeview_sortie_hostname = gtk.TreeView(self.liststore_hostname)
        treeview_sortie_hostname.set_rules_hint(True)
        treeview_sortie_hostname.append_column(gtk.TreeViewColumn("Adresse IP", gtk.CellRendererText(), text=0))
        treeview_sortie_hostname.append_column(gtk.TreeViewColumn("Hostname", gtk.CellRendererText(), text=1))
        scrolled_sortie_hostname.add(treeview_sortie_hostname)
        scrolled_sortie_hostname.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        treeview_sortie_hostname.show()

        # boite2_hostname
        boite2_hostname = gtk.HBox(False, 5)
        boite1_hostname.pack_start(boite2_hostname, False, False, 0)
        boite2_hostname.show()

        # self.progressbarHostname
        self.progressbarHostname = gtk.ProgressBar()
        self.progressbarHostname.set_text("En attente ...")
        boite2_hostname.pack_start(self.progressbarHostname, True, True, 0)
        self.progressbarHostname.show()

        # self.btn_hostname
        self.btn_hostname = gtk.Button("Check")
        self.btn_hostname.set_size_request(int(self.btn_hostname.size_request()[0]*1.1),self.btn_hostname.size_request()[1])
        boite2_hostname.pack_start(self.btn_hostname, False, False, 0)
        self.btn_hostname.connect("clicked", lambda e: thread.start_new_thread(self.hostname, ()))
        self.btn_hostname.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_hostname, gtk.Label("Hostname Resolver"), -1)

    def wifiView(self):
        iface=self.combo_iface_wifi.get_active_text().split()[0]

        if self.enCoursWifi:
            self.enCoursWifi=0
            self.btn_wifi.set_label("Start")
        elif not getoutput("which iw"):
            os_info=getoutput("uname -a").lower()
            alert="Un outils est nécessaire, veuillez l'installer :\niw - tool for configuring Linux wireless devices"
            alert+=''.join(["\n\n# apt-get install iw" for os in "backtrack","debian","ubuntu","mint","voyager" if os in os_info and not "apt-get" in alert])
            alert+=''.join(["\n\n# yum install iw\n(à vérifier)" for os in "fedora","centos" if os in os_info and not "yum" in alert])
            gtk.gdk.threads_enter()
            self.msgbox(alert,1)
            gtk.gdk.threads_leave()
        elif "(-19)" in getoutput("iw "+iface+" info"):
            gtk.gdk.threads_enter()
            self.btn_wifi.set_label("Start")
            self.msgbox("Veuillez sélectionner une interface Wi-Fi !",1)
            gtk.gdk.threads_leave()
            self.enCoursWifi=0
        else:
            # Vérification des permissions
            for su_gui_cmd in ['gksu','kdesu','ktsuss','beesu','']:
                if getoutput("which "+su_gui_cmd): break
            if not su_gui_cmd:
                gtk.gdk.threads_enter()
                self.msgbox("Un des outils suivant est nécessaire pour acquérir les droits administrateur, veuillez en installer un :\n\ngksu\nkdesu\nktsuss\nbeesu",1)
                gtk.gdk.threads_leave()
            else:
                self.enCoursWifi=1
                thread.start_new_thread(self.runProgressbarWifi, ())
                self.btn_wifi.set_label("Stop")
                self.progressbarWifi.set_text("Scan en cours ...")

                rssiMin=-120
                rssiMax=-30
                while self.enCoursWifi and su_gui_cmd:
                    iwOut=getoutput(su_gui_cmd+" iw dev "+iface+" scan")

                    if not iwOut:
                        continue
                    if "(-1)" in iwOut:
                        gtk.gdk.threads_enter()
                        self.btn_wifi.set_label("Start")
                        self.msgbox("Nécessite d'être lancé en tant qu'administrateur !",1)
                        gtk.gdk.threads_leave()
                        self.enCoursWifi=0
                    elif "(-100)" in iwOut:
                        gtk.gdk.threads_enter()
                        self.btn_wifi.set_label("Start")
                        self.msgbox("L'interface Wi-Fi séléctionnée est désactivée !",1)
                        gtk.gdk.threads_leave()
                        self.enCoursWifi=0
                    else:
                        res = re.compile('BSS ([\w\d\:]+).*\n.*\n.*\n.*\n.*\n\tsignal: ([-\.\d]+) dBm\n\tlast seen: (\d+) ms ago\n\tSSID: (.*)\n', re.MULTILINE).findall(iwOut)
                        if len(res)!=len(re.compile('signal: ([-\.\d]+ dBm)\n', re.MULTILINE).findall(iwOut)): print "Problème !"

                        for x in res:
                            found=0
                            apIter=self.liststore_wifi.get_iter_first() # None quand liststore vide
                            while apIter:
                                if self.liststore_wifi.get_value(apIter, 1) == x[0]:
                                    self.liststore_wifi.set(apIter, 2, x[1], 3, int((float(x[1])-rssiMin))*100/(rssiMax-rssiMin)) # Modifier une ligne
                                    if int(x[2])>5000: self.liststore_wifi.set(apIter, 2, '', 3, 0) # Modifier une ligne
                                    found=1
                                apIter=self.liststore_wifi.iter_next(apIter)
                            else:
                                if not found:
                                    self.liststore_wifi.append([x[3],x[0],x[1],int((float(x[1])-rssiMin))*100/(rssiMax-rssiMin)])
                                    print int((float(x[1])-rssiMin))*100/(rssiMax-rssiMin)

    def tabWifi(self): # TAB Wi-Fi
    # boites
        boite1_wifi = gtk.VBox(False, 5)
        boite1_wifi.show()

        # self.liststore_wifi
        self.liststore_wifi = gtk.ListStore(str, str, str, int)
        # scrollbar_sortie_wifi
        scrolled_sortie_wifi = gtk.ScrolledWindow()
        boite1_wifi.pack_start(scrolled_sortie_wifi, True, True, 0)
        scrolled_sortie_wifi.show()
        # self.treeview_sortie_wifi
        treeview_sortie_wifi = gtk.TreeView(self.liststore_wifi)
        treeview_sortie_wifi.set_rules_hint(True)
        treeview_sortie_wifi.append_column(gtk.TreeViewColumn("SSID", gtk.CellRendererText(), text=0))
        treeview_sortie_wifi.append_column(gtk.TreeViewColumn("MAC", gtk.CellRendererText(), text=1))
        treeview_sortie_wifi.append_column(gtk.TreeViewColumn("RSSI (dBm)", gtk.CellRendererText(), text=2))
        treeview_sortie_wifi.append_column(gtk.TreeViewColumn("Signal", gtk.CellRendererProgress(), value=3))

        treeview_sortie_wifi.set_reorderable(True)
        #        self.liststore_wifi.set_sort_column_id(3, gtk.SORT_DESCENDING)

        scrolled_sortie_wifi.add(treeview_sortie_wifi)
        scrolled_sortie_wifi.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        treeview_sortie_wifi.show()

        # boite2_wifi
        boite2_wifi = gtk.HBox(False, 5)
        boite1_wifi.pack_start(boite2_wifi, False, False, 0)
        boite2_wifi.show()

        # self.progressbarWifi
        self.progressbarWifi = gtk.ProgressBar()
        self.progressbarWifi.set_text("En attente ...")
        boite2_wifi.pack_start(self.progressbarWifi, True, True, 0)
        self.progressbarWifi.show()

        # self.combo_iface_wifi
        self.combo_iface_wifi = gtk.combo_box_new_text()
        boite2_wifi.pack_start(self.combo_iface_wifi, False, False, 0)
        self.combo_iface_wifi.show()

        # self.btn_wifi
        self.btn_wifi = gtk.Button("Start")
        self.btn_wifi.set_size_request(int(self.btn_wifi.size_request()[0]*1.1),self.btn_wifi.size_request()[1])
        boite2_wifi.pack_start(self.btn_wifi, False, False, 0)
        self.btn_wifi.connect("clicked", lambda e: thread.start_new_thread(self.wifiView, ()))
        self.btn_wifi.show()

        self.enCoursWifi=0

        # Affichage
        self.bloc_tabs.insert_page(boite1_wifi, gtk.Label("Wi-Fi Scanner"), -1)

    def wifiView2(self):
        iface=self.combo_iface_wifi2.get_active_text().split()[0]

        if self.enCoursWifi2:
            self.enCoursWifi2=0
            self.btn_wifi2.set_label("Start")
        elif not getoutput("which airodump-ng"):
            os_info=getoutput("uname -a").lower()
            alert="Un outils est nécessaire, veuillez l'installer :\naircrack-ng - Utilitaires de crackage de clefs WEP/WPA"
            alert+=''.join(["\n\n# apt-get install aircrack-ng" for os in "backtrack","debian","ubuntu","mint" if os in os_info and not "apt-get" in alert])
            alert+=''.join(["\n\n# yum install aircrack-ng\n(à vérifier)" for os in "fedora","centos" if os in os_info and not "yum" in alert])
            gtk.gdk.threads_enter()
            self.msgbox(alert,1)
            gtk.gdk.threads_leave()
        elif not getoutput("which iw"):
            os_info=getoutput("uname -a").lower()
            alert="Un outils est nécessaire, veuillez l'installer :\niw - tool for configuring Linux wireless devices"
            alert+=''.join(["\n\n# apt-get install iw" for os in "backtrack","debian","ubuntu","mint","voyager" if os in os_info and not "apt-get" in alert])
            alert+=''.join(["\n\n# yum install iw\n(à vérifier)" for os in "fedora","centos" if os in os_info and not "yum" in alert])
            gtk.gdk.threads_enter()
            self.msgbox(alert,1)
            gtk.gdk.threads_leave()
        elif not "monitor" in getoutput("iw "+iface+" info"):
            gtk.gdk.threads_enter()
            self.btn_wifi.set_label("Start")
            self.msgbox("Veuillez sélectionner une interface Wi-Fi en mode moniteur !",1)
            gtk.gdk.threads_leave()
            self.enCoursWifi2=0
        else:
            # Vérification des permissions
            for su_gui_cmd in ['gksu','kdesu','ktsuss','beesu','']:
                if getoutput("which "+su_gui_cmd): break
            if not su_gui_cmd:
                gtk.gdk.threads_enter()
                self.msgbox("Un des outils suivant est nécessaire pour acquérir les droits administrateur, veuillez en installer un :\n\ngksu\nkdesu\nktsuss\nbeesu",1)
                gtk.gdk.threads_leave()
            else:
                self.enCoursWifi2=1
                thread.start_new_thread(self.runProgressbarWifi2, ())
                self.btn_wifi2.set_label("Stop")
                self.progressbarWifi2.set_text("Scan en cours ...")

                rssiMin=-120
                rssiMax=-30

                t_airodump = thread.start_new_thread(getstatusoutput, (su_gui_cmd+" \"airodump-ng "+iface+" --write '%s/tmp/airodump-ng' --output-format csv -u 1\"" % FKTB_PATH,))

                while self.enCoursWifi2 and su_gui_cmd:
                    try:
                        with open("%s/tmp/airodump-ng-01.csv" % FKTB_PATH, 'rb') as f:
                            reader = csv.reader(f)
                            for x in reader:
                                if x:
                                    if len(x) == 15 and re.sub('[\s]+$','',re.sub('^[\s]+','',x[0])) != "BSSID": # grande ligne
                                        found=0
                                        apIter=self.liststore_wifi2.get_iter_first() # None quand liststore vide
                                        while apIter:
                                            if self.liststore_wifi2.get_value(apIter, 1) == re.sub('[\s]+$','',re.sub('^[\s]+','',x[0])):
                                                power=int((float(re.sub('[\s]+$','',re.sub('^[\s]+','',x[8])))-rssiMin))*100/(rssiMax-rssiMin)
                                                if power > 100: power=100
                                                self.liststore_wifi2.set(apIter, 2, power,
                                                                         3, re.sub('[\s]+$','',re.sub('^[\s]+','',x[2])),
                                                                         9, re.sub('[\s]+$','',re.sub('^[\s]+','',x[9])),
                                                                         10, re.sub('[\s]+$','',re.sub('^[\s]+','',x[10])),
                                                                         11, re.sub('[\s]+$','',re.sub('^[\s]+','',x[11])),
                                                                         12, re.sub('[\s]+$','',re.sub('^[\s]+','',x[12])),
                                                                         14, re.sub('[\s]+$','',re.sub('^[\s]+','',x[14]))) # Modifier une ligne
                                                #if int(x[2])>5000: self.liststore_wifi2.set(apIter, 9, 0) # Modifier une ligne
                                                found=1
                                            apIter=self.liststore_wifi2.iter_next(apIter)
                                        else:
                                            if not found:
                                                power=int((float(re.sub('[\s]+$','',re.sub('^[\s]+','',x[8])))-rssiMin))*100/(rssiMax-rssiMin)
                                                if power > 100: power=100
                                                self.liststore_wifi2.append([re.sub('[\s]+$','',re.sub('^[\s]+','',x[13])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[0])),
                                                                             power,
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[2])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[5])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[6])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[7])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[3])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[4])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[9])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[10])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[11])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[12])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[1])),
                                                                             re.sub('[\s]+$','',re.sub('^[\s]+','',x[14]))])
                                    elif len(x) == 7 and re.sub('[\s]+$','',re.sub('^[\s]+','',x[0])) != "Station MAC": # petite ligne
                                        found=0
                                        apIter=self.liststore_wifi22.get_iter_first() # None quand liststore vide
                                        while apIter:
                                            if self.liststore_wifi22.get_value(apIter, 0) == re.sub('[\s]+$','',re.sub('^[\s]+','',x[0])):
                                                power=int((float(re.sub('[\s]+$','',re.sub('^[\s]+','',x[3])))-rssiMin))*100/(rssiMax-rssiMin)
                                                if power > 100: power=100
                                                self.liststore_wifi22.set(apIter, 2, re.sub('[\s]+$','',re.sub('^[\s]+','',x[2])),
                                                                          3, power,
                                                                          4, re.sub('[\s]+$','',re.sub('^[\s]+','',x[4])),
                                                                          5, re.sub('[\s]+$','',re.sub('^[\s]+','',x[5])),
                                                                          6, re.sub('[\s]+$','',re.sub('^[\s]+','',x[6]))) # Modifier une ligne
                                                #if int(x[2])>5000: self.liststore_wifi22.set(apIter, 9, 0) # Modifier une ligne
                                                found=1
                                            apIter=self.liststore_wifi22.iter_next(apIter)
                                        else:
                                            if not found:
                                                power=int((float(re.sub('[\s]+$','',re.sub('^[\s]+','',x[3])))-rssiMin))*100/(rssiMax-rssiMin)
                                                if power > 100: power=100
                                                self.liststore_wifi22.append([re.sub('[\s]+$','',re.sub('^[\s]+','',x[0])),
                                                                              re.sub('[\s]+$','',re.sub('^[\s]+','',x[1])),
                                                                              re.sub('[\s]+$','',re.sub('^[\s]+','',x[2])),
                                                                              power,
                                                                              re.sub('[\s]+$','',re.sub('^[\s]+','',x[4])),
                                                                              re.sub('[\s]+$','',re.sub('^[\s]+','',x[5])),
                                                                              re.sub('[\s]+$','',re.sub('^[\s]+','',x[6]))])
                    except IOError: continue
                    sleep(1)

    def tabWifi2(self): # TAB Wi-Fi 2
    # boites
        boite1_wifi2 = gtk.VBox(False, 5)
        boite1_wifi2.show()

        # self.liststore_wifi2
        self.liststore_wifi2 = gtk.ListStore(str, str, int, str, str, str, str, str, str, str, str, str, str, str, str)
        # scrollbar_sortie_wifi2
        scrolled_sortie_wifi2 = gtk.ScrolledWindow()
        boite1_wifi2.pack_start(scrolled_sortie_wifi2, True, True, 0)
        scrolled_sortie_wifi2.show()
        # self.treeview_sortie_wifi2
        treeview_sortie_wifi2 = gtk.TreeView(self.liststore_wifi2)
        treeview_sortie_wifi2.set_rules_hint(True)

        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("ESSID", gtk.CellRendererText(), text=0))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("BSSID", gtk.CellRendererText(), text=1))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("Power", gtk.CellRendererProgress(), value=2))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("Last time seen", gtk.CellRendererText(), text=3))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("Privacy", gtk.CellRendererText(), text=4))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("Cipher", gtk.CellRendererText(), text=5))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("Authentication", gtk.CellRendererText(), text=6))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("channel", gtk.CellRendererText(), text=7))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("Speed", gtk.CellRendererText(), text=8))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("# beacons", gtk.CellRendererText(), text=9))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("# IV", gtk.CellRendererText(), text=10))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("LAN IP", gtk.CellRendererText(), text=11))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("ID-length", gtk.CellRendererText(), text=12))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("First time seen", gtk.CellRendererText(), text=13))
        treeview_sortie_wifi2.append_column(gtk.TreeViewColumn("Key", gtk.CellRendererText(), text=14))

        treeview_sortie_wifi2.set_reorderable(True)
        #        self.liststore_wifi2.set_sort_column_id(8, gtk.SORT_DESCENDING)

        scrolled_sortie_wifi2.add(treeview_sortie_wifi2)
        scrolled_sortie_wifi2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        treeview_sortie_wifi2.show()

        # self.liststore_wifi22
        self.liststore_wifi22 = gtk.ListStore(str, str, str, int, str, str, str)
        # scrollbar_sortie_wifi22
        scrolled_sortie_wifi22 = gtk.ScrolledWindow()
        boite1_wifi2.pack_start(scrolled_sortie_wifi22, True, True, 0)
        scrolled_sortie_wifi22.show()
        # self.treeview_sortie_wifi22
        treeview_sortie_wifi22 = gtk.TreeView(self.liststore_wifi22)
        treeview_sortie_wifi22.set_rules_hint(True)

        treeview_sortie_wifi22.append_column(gtk.TreeViewColumn("Station MAC", gtk.CellRendererText(), text=0))
        treeview_sortie_wifi22.append_column(gtk.TreeViewColumn("First time seen", gtk.CellRendererText(), text=1))
        treeview_sortie_wifi22.append_column(gtk.TreeViewColumn("Last time seen", gtk.CellRendererText(), text=2))
        treeview_sortie_wifi22.append_column(gtk.TreeViewColumn("Power", gtk.CellRendererProgress(), value=3))
        treeview_sortie_wifi22.append_column(gtk.TreeViewColumn("# packets", gtk.CellRendererText(), text=4))
        treeview_sortie_wifi22.append_column(gtk.TreeViewColumn("BSSID", gtk.CellRendererText(), text=5))
        treeview_sortie_wifi22.append_column(gtk.TreeViewColumn("Probed ESSIDs", gtk.CellRendererText(), text=6))

        treeview_sortie_wifi22.set_reorderable(True)
        #        self.liststore_wifi22.set_sort_column_id(0, gtk.SORT_DESCENDING)

        scrolled_sortie_wifi22.add(treeview_sortie_wifi22)
        scrolled_sortie_wifi22.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        treeview_sortie_wifi22.show()


        # boite2_wifi2
        boite2_wifi2 = gtk.HBox(False, 5)
        boite1_wifi2.pack_start(boite2_wifi2, False, False, 0)
        boite2_wifi2.show()

        # self.progressbarWifi2
        self.progressbarWifi2 = gtk.ProgressBar()
        self.progressbarWifi2.set_text("En attente ...")
        boite2_wifi2.pack_start(self.progressbarWifi2, True, True, 0)
        self.progressbarWifi2.show()

        # self.combo_iface_wifi2
        self.combo_iface_wifi2 = gtk.combo_box_new_text()
        boite2_wifi2.pack_start(self.combo_iface_wifi2, False, False, 0)
        self.combo_iface_wifi2.show()

        # self.btn_wifi2
        self.btn_wifi2 = gtk.Button("Start")
        self.btn_wifi2.set_size_request(int(self.btn_wifi2.size_request()[0]*1.1),self.btn_wifi2.size_request()[1])
        boite2_wifi2.pack_start(self.btn_wifi2, False, False, 0)
        self.btn_wifi2.connect("clicked", lambda e: thread.start_new_thread(self.wifiView2, ()))
        self.btn_wifi2.show()

        self.enCoursWifi2=0

        # Affichage
        self.bloc_tabs.insert_page(boite1_wifi2, gtk.Label("Wi-Fi Scanner 2"), -1)

    def consecutiveMaj(self, pwd):
        nbConsecutiveMaj=0
        for x in range(1,len(pwd)):
            if pwd[x].isupper() and pwd[x-1].isupper(): nbConsecutiveMaj+=1
        return nbConsecutiveMaj

    def consecutiveMin(self, pwd):
        nbConsecutiveMin=0
        for x in range(1,len(pwd)):
            if pwd[x].islower() and pwd[x-1].islower(): nbConsecutiveMin+=1
        return nbConsecutiveMin

    def consecutiveNum(self, pwd):
        nbConsecutiveNum=0
        for x in range(1,len(pwd)):
            if pwd[x] in "0123456789" and pwd[x-1] in "0123456789": nbConsecutiveNum+=1
        return nbConsecutiveNum

    def sequencialChar(self, pwd):
        nbSequencialChar=0
        for x in range(1,len(pwd)):
            if ord(pwd[x])-ord(pwd[x-1])==1: nbSequencialChar+=1
        if nbSequencialChar >= 2: nbSequencialChar-=1
        else: nbSequencialChar=0
        return nbSequencialChar

    def repeatChar(self, pwd):
        nbRepeatChar=0
        for c in pwd:
            nbRepeatChar+=pwd.count(c)-1
        return nbRepeatChar

    def checkPwdStrenght(self):
        self.liststore_pwdStrenght.clear()
        pwd=self.entry_pwdStrenght.get_text()
        if pwd:
            # Problème quand on écrit des caractère trops vite !?
            somme=0
            nbMin=0
            nbMaj=0
            nbNum=0
            nbSpec=0
            nbMiddleNumOrSpec=0
            nbDiffType=0

            for x in range(0,len(pwd)):
                if pwd[x] in "abcdefghijklmnopqrstuvwxyz": nbMin = nbMin + 1
                if pwd[x] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": nbMaj = nbMaj + 1
                if pwd[x] in "0123456789":
                    nbNum+=1
                    if x > 0 and x < len(pwd)-1: nbMiddleNumOrSpec+=1
                if pwd[x] in "`!\"?$?%^&*()_-+={[}]:;@'~#|\<,>.?/":
                    nbSpec+=1
                    if x > 0 and x < len(pwd)-1: nbMiddleNumOrSpec+=1

            if nbMin: nbDiffType+=1
            if nbMaj: nbDiffType+=1
            if nbNum: nbDiffType+=1
            if nbSpec: nbDiffType+=1

            somme+=len(pwd)*4
            self.liststore_pwdStrenght.append(("Nombre de caractères", str(len(pwd))+" (+"+str(somme)+")"))

            if nbMaj:
                somme+=(len(pwd)-nbMaj)*2
                if (len(pwd)-nbMaj)*2>0: self.liststore_pwdStrenght.append(("Lettres majuscules", str(nbMaj)+" (+"+str((len(pwd)-nbMaj)*2)+")"))
                else: self.liststore_pwdStrenght.append(("Lettres majuscules", str(nbMaj)))
            else: self.liststore_pwdStrenght.append(("Lettres majuscules", str(nbMaj)))

            if nbMin:
                somme+=(len(pwd)-nbMin)*2
                if (len(pwd)-nbMin)*2>0: self.liststore_pwdStrenght.append(("Lettres minuscules", str(nbMin)+" (+"+str((len(pwd)-nbMin)*2)+")"))
                else: self.liststore_pwdStrenght.append(("Lettres minuscules", str(nbMin)))
            else: self.liststore_pwdStrenght.append(("Lettres minuscules", str(nbMin)))

            if nbNum and (nbMin or nbMaj or nbSpec):
                somme+=nbNum*4
                self.liststore_pwdStrenght.append(("Chiffres", str(nbNum)+" (+"+str(nbNum*4)+")"))
            else: self.liststore_pwdStrenght.append(("Chiffres", "0"))

            if nbSpec*6:
                somme+=nbSpec*6
                self.liststore_pwdStrenght.append(("Symboles", str(nbSpec)+" (+"+str(nbSpec*6)+")"))
            else: self.liststore_pwdStrenght.append(("Symboles", str(nbSpec)))

            if nbMiddleNumOrSpec*2:
                somme+=nbMiddleNumOrSpec*2
                self.liststore_pwdStrenght.append(("Chiffres ou symboles au milieu", str(nbMiddleNumOrSpec)+" (+"+str(nbMiddleNumOrSpec*2)+")"))
            else : self.liststore_pwdStrenght.append(("Chiffres ou symboles au milieu", str(nbMiddleNumOrSpec)))

            # problème quand >=8 (aaaaaaA & aaaaaaaA)
            if len(pwd) >= 8 and nbDiffType >= 3:
                somme+=(nbDiffType+1)*2
                self.liststore_pwdStrenght.append(("Exigences", str(nbDiffType+1)+" (+"+str((nbDiffType+1)*2)+")"))
            else: self.liststore_pwdStrenght.append(("Exigences", str(nbDiffType)))

            if (nbMin or nbMaj) and not nbNum and not nbSpec:
                somme-=nbMin+nbMaj
                self.liststore_pwdStrenght.append(("Lettres seulement", str(nbMin+nbMaj)+" (-"+str(nbMin+nbMaj)+")"))
            else: self.liststore_pwdStrenght.append(("Lettres seulement", "0"))
            if nbNum and not nbMin and not nbMaj and not nbSpec:
                somme-=nbNum
                self.liststore_pwdStrenght.append(("Chiffres seulement", str(nbNum)+" (-"+str(nbNum)+")"))
            else: self.liststore_pwdStrenght.append(("Chiffres seulement", "0"))


            if self.repeatChar(pwd):
                somme-=self.repeatChar(pwd)
                self.liststore_pwdStrenght.append(("Répétition de caractères (insensible à la casse)", str(self.repeatChar(pwd))+" (-"+str(self.repeatChar(pwd))+")"))
            else: self.liststore_pwdStrenght.append(("Répétition de caractères (insensible à la casse)", str(self.repeatChar(pwd))))

            if self.consecutiveMaj(pwd)*2:
                somme-=self.consecutiveMaj(pwd)*2
                self.liststore_pwdStrenght.append(("Lettres majuscules consécutives", str(self.consecutiveMaj(pwd))+" (-"+str(self.consecutiveMaj(pwd)*2)+")"))
            else: self.liststore_pwdStrenght.append(("Lettres majuscules consécutives", str(self.consecutiveMaj(pwd))))

            if self.consecutiveMin(pwd)*2:
                somme-=self.consecutiveMin(pwd)*2
                self.liststore_pwdStrenght.append(("Lettres minuscules consécutives", str(self.consecutiveMin(pwd))+" (-"+str(self.consecutiveMin(pwd)*2)+")"))
            else: self.liststore_pwdStrenght.append(("Lettres minuscules consécutives", str(self.consecutiveMin(pwd))))

            if self.consecutiveNum(pwd)*2:
                somme-=self.consecutiveNum(pwd)*2
                self.liststore_pwdStrenght.append(("Chiffres consécutifs", str(self.consecutiveNum(pwd))+" (-"+str(self.consecutiveNum(pwd)*2)+")"))
            else: self.liststore_pwdStrenght.append(("Chiffres consécutifs", str(self.consecutiveNum(pwd))))

            if self.sequencialChar(pwd)*3:
                somme-=self.sequencialChar(pwd)*3
                self.liststore_pwdStrenght.append(("Caractères séquentiels (3+)",str(self.sequencialChar(pwd))+" (-"+str(self.sequencialChar(pwd)*3)+")"))
            else: self.liststore_pwdStrenght.append(("Caractères séquentiels (3+)",str(self.sequencialChar(pwd))))

            if somme > 100: somme=100
            elif somme < 0: somme=0
            self.liststore_pwdStrenght.append(("", ""))
            self.liststore_pwdStrenght.append(("Force du mot de passe", str(somme)+" %"))

    def tabPwdStrenght(self): # TAB Password Strenght
    # boites
        boite1_pwdStrenght = gtk.VBox(False, 5)
        boite1_pwdStrenght.show()

        # self.label_pwdStrenght
        self.label_pwdStrenght = gtk.Label("Calculer la force d'un mot de passe (beta) :")
        self.label_pwdStrenght.set_alignment(0,0)
        boite1_pwdStrenght.pack_start(self.label_pwdStrenght, False, False, 0)
        self.label_pwdStrenght.show()

        # boite2_pwdStrenght
        boite2_pwdStrenght = gtk.HBox(False, 5)
        boite1_pwdStrenght.pack_start(boite2_pwdStrenght, False, False, 0)
        boite2_pwdStrenght.show()

        # self.entry_pwdStrenght
        self.entry_pwdStrenght = gtk.Entry()
        boite2_pwdStrenght.pack_start(self.entry_pwdStrenght, True, True, 0)
        self.entry_pwdStrenght.connect("changed", lambda e: thread.start_new_thread(self.checkPwdStrenght, ()))
        self.entry_pwdStrenght.show()

        # self.liststore_pwdStrenght
        self.liststore_pwdStrenght = gtk.ListStore(str, str)
        # scrollbar_sortie_pwdStrenght
        scrolled_sortie_pwdStrenght = gtk.ScrolledWindow()
        boite1_pwdStrenght.pack_start(scrolled_sortie_pwdStrenght, True, True, 0)
        scrolled_sortie_pwdStrenght.show()
        # self.self.treeview_pwdStrenght
        self.treeview_pwdStrenght = gtk.TreeView(self.liststore_pwdStrenght)
        self.treeview_pwdStrenght.set_rules_hint(True)
        self.treeview_pwdStrenght.append_column(gtk.TreeViewColumn(None, gtk.CellRendererText(), text=0))
        self.treeview_pwdStrenght.append_column(gtk.TreeViewColumn(None, gtk.CellRendererText(), text=1))
        self.treeview_pwdStrenght.set_headers_visible(False)

        scrolled_sortie_pwdStrenght.add(self.treeview_pwdStrenght)
        scrolled_sortie_pwdStrenght.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.treeview_pwdStrenght.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_pwdStrenght, gtk.Label("Password Strenght"), -1)

    def tabBarCode(self): # TAB Code-barres
    # boites
        boite1_barCode = gtk.VBox(False, 5)
        boite1_barCode.show()

        # self.label_barCode
        self.label_barCode = gtk.Label("Lecteur de code-barres :")
        self.label_barCode.set_alignment(0,0)
        boite1_barCode.pack_start(self.label_barCode, False, False, 0)
        self.label_barCode.show()

        # self.btn_barCode
        self.btn_barCode = gtk.Button("ouvrir")
        self.btn_barCode.set_size_request(int(self.btn_barCode.size_request()[0]*1.2),self.btn_barCode.size_request()[1])
        self.btn_barCode.connect("clicked", lambda e: subprocess.Popen(("python","%s/lib/other/zbar.py" % FKTB_PATH), stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        boite1_barCode.pack_start(self.btn_barCode, False, False, 0)
        self.btn_barCode.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_barCode, gtk.Label("Code-barres"), -1)

    def tabGeoloc(self): # TAB Google Wi-Fi Positioning System
    # boites
        boite1_geoloc = gtk.VBox(False, 5)
        boite1_geoloc.show()

        # self.label_geoloc
        self.label_geoloc = gtk.Label("Google Wi-Fi Positioning System :")
        self.label_geoloc.set_alignment(0,0)
        boite1_geoloc.pack_start(self.label_geoloc, False, False, 0)
        self.label_geoloc.show()

        class DummyMapNoGpsPoint(osmgpsmap.GpsMap):
            def do_draw_gps_point(self, drawable):
                pass
        gobject.type_register(DummyMapNoGpsPoint)

        class DummyLayer(gobject.GObject, osmgpsmap.GpsMapLayer):
            def __init__(self):
                gobject.GObject.__init__(self)

            def do_draw(self, gpsmap, gdkdrawable):
                pass

            def do_render(self, gpsmap):
                pass

            def do_busy(self):
                return False

            def do_button_press(self, gpsmap, gdkeventbutton):
                return False
        gobject.type_register(DummyLayer)

        if 0:
            self.osm = DummyMapNoGpsPoint()
        else:
            self.osm = osmgpsmap.GpsMap()
        self.osm.layer_add(
            osmgpsmap.GpsMapOsd(
                show_dpad=True,
                show_zoom=True))
        self.osm.layer_add(
            DummyLayer())

        #connect keyboard shortcutsf
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_FULLSCREEN, gtk.gdk.keyval_from_name("F11"))
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_UP, gtk.gdk.keyval_from_name("Up"))
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_DOWN, gtk.gdk.keyval_from_name("Down"))
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_LEFT, gtk.gdk.keyval_from_name("Left"))
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_RIGHT, gtk.gdk.keyval_from_name("Right"))

        self.osm.show()

        boite1_geoloc.pack_start(self.osm, True, True, 0)

        #gobject.timeout_add(500, self.print_tiles)
        self.osm.set_center_and_zoom(46.227638, 2.213749, 5) # Centrer sur la France

        ex = gtk.Expander("<b>Historique</b>")
        ex.props.use_markup = True

        vb = gtk.VBox()
        ex.add(vb)

        self.debug_button = gtk.Button("Commencer la géolocalisation")
        self.debug_button.connect('clicked', lambda e: thread.start_new_thread(self.debug_clicked, ()))

        hbox = gtk.HBox(True, 0)

        # self.liststore_geoloc
        self.liststore_geoloc = gtk.ListStore( str, str)
        # scrollbar_sortie_geoloc
        scrolled_sortie_geoloc = gtk.ScrolledWindow()
        hbox.pack_start(scrolled_sortie_geoloc, True, True, 0)
        scrolled_sortie_geoloc.show()
        # self.treeasview_sortie_geoloc
        self.treeview_sortie_geoloc = gtk.TreeView(self.liststore_geoloc)
        self.treeview_sortie_geoloc.set_rules_hint(True)
        self.treeview_sortie_geoloc.append_column(gtk.TreeViewColumn("Heure", gtk.CellRendererText(), text=0))
        self.treeview_sortie_geoloc.append_column(gtk.TreeViewColumn("Position", gtk.CellRendererText(), text=1))
        self.treeview_sortie_geoloc.set_headers_visible(False)
        self.treeview_sortie_geoloc.connect("cursor-changed", self.locHistory)
        scrolled_sortie_geoloc.add(self.treeview_sortie_geoloc)
        scrolled_sortie_geoloc.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.treeview_sortie_geoloc.show()

        vb.pack_start(hbox, True)

        boite1_geoloc.pack_start(ex, False, True, 0)

        hbox.show()
        vb.show()
        ex.show()

        # boite2_geoloc
        boite2_geoloc = gtk.HBox(False, 5)
        boite1_geoloc.pack_start(boite2_geoloc, False, False, 0)
        boite2_geoloc.show()

        # self.combo_iface_geoloc
        self.combo_iface_geoloc = gtk.combo_box_new_text()
        boite2_geoloc.pack_start(self.combo_iface_geoloc, False, False, 0)
        self.combo_iface_geoloc.show()

        # self.btn_geoloc
        self.btn_geoloc = gtk.Button("Lancer la géolocalisation")
        self.btn_geoloc.set_size_request(int(self.btn_geoloc.size_request()[0]*1.2),self.btn_geoloc.size_request()[1])
        self.btn_geoloc.connect('clicked', lambda e: thread.start_new_thread(self.geoloc, ()))
        boite2_geoloc.pack_start(self.btn_geoloc, True, True, 0)
        self.btn_geoloc.show()

        # self.btn2_geoloc
        self.btn2_geoloc = gtk.Button("en boucle")
        self.btn2_geoloc.set_size_request(int(self.btn2_geoloc.size_request()[0]*1.2),self.btn2_geoloc.size_request()[1])
        self.statuGeolocLoop=False
        self.btn2_geoloc.connect('clicked', lambda e: thread.start_new_thread(self.geolocLoop, ()))
        boite2_geoloc.pack_start(self.btn2_geoloc, False, False, 0)
        self.btn2_geoloc.show()

        # Affichage
        self.bloc_tabs.insert_page(boite1_geoloc, gtk.Label("Google Wi-Fi\nPositioning System"), -1)

    def locHistory(self, parent):
        try: choix = self.liststore_geoloc.get_value(self.treeview_sortie_geoloc.get_selection().get_selected()[1], 1)
        except TypeError: pass
        else:
            result=re.compile("longitude : ([\d\:\.-]+), latitude : ([\d\:\.-]+)", re.MULTILINE).findall(choix)
            #print result[0][0]+", "+result[0][1]
            self.osm.set_center_and_zoom(float(result[0][1]), float(result[0][0]), 16)

    def geolocLoop(self):
        if self.statuGeolocLoop:
            self.statuGeolocLoop=False
            self.btn2_geoloc.set_label("en boucle")
            if "secondes" in self.btn_geoloc.get_label():
                self.btn_geoloc.set_label("Lancer la géolocalisation")
                self.btn_geoloc.set_sensitive(True)
        else:
            self.statuGeolocLoop=True
            self.btn2_geoloc.set_label("stop")
            while self.statuGeolocLoop:
                self.geoloc()
                sleep(5)

    def geoloc(self):
        """Google Wi-Fi Positioning System"""

        iface=self.combo_iface_geoloc.get_active_text().split()[0]

        if not getoutput("which iw"):
            os_info=getoutput("uname -a").lower()
            alert="Un outils est nécessaire, veuillez l'installer :\niw - tool for configuring Linux wireless devices"
            alert+=''.join(["\n\n# apt-get install iw" for os in "backtrack","debian","ubuntu","mint","voyager" if os in os_info and not "apt-get" in alert])
            alert+=''.join(["\n\n# yum install iw\n(à vérifier)" for os in "fedora","centos" if os in os_info and not "yum" in alert])
            gtk.gdk.threads_enter()
            self.msgbox(alert,1)
            gtk.gdk.threads_leave()
        else:
            self.btn_geoloc.set_sensitive(False)
            self.btn_geoloc.set_label("Scan des réseaux Wi-Fi à proximité ...")

            # Vérification des permissions
            for su_gui_cmd in ['gksu','kdesu','ktsuss','beesu','']:
                if getoutput("which "+su_gui_cmd): break
            if not su_gui_cmd:
                gtk.gdk.threads_enter()
                self.msgbox("Un des outils suivant est nécessaire pour acquérir les droits administrateur, veuillez en installer un :\n\ngksu\nkdesu\nktsuss\nbeesu",1)
                gtk.gdk.threads_leave()
            else: iwOut=getoutput(su_gui_cmd+" iw dev "+iface+" scan")

            if "failed" in iwOut:
                if not self.statuGeolocLoop:
                    self.statuGeolocLoop=False
                    self.btn_geoloc.set_label("Lancer la géolocalisation")
                    self.btn_geoloc.set_sensitive(True)
                    gtk.gdk.threads_enter()
                    self.msgbox("Le scan des réseaux Wi-Fi a échoué.\n\nVérifiez votre carte réseau sans fils !",1)
                    gtk.gdk.threads_leave()
                else: self.btn_geoloc.set_label("Echec du scan, nouvel essai dans 5 secondes ...")
            else:
                result=re.compile("BSS ([\w\d\:]+).*\n.*\n.*\n.*\n.*\n\tsignal: ([-\d]+)", re.MULTILINE).findall(iwOut)

                self.btn_geoloc.set_label("Génération de la requête ...")

                loc_req={ "version":"1.1.0",
                          "request_address":False,
                          #"addresults_language":"fr",
                          "wifi_towers":[{"mac_address":x[0].replace(":","-"),"signal_strength":int(x[1])} for x in result]
                }

                #print '\n'.join([l.rstrip() for l in simplejson.dumps(loc_req, sort_keys=True, indent=4*' ').splitlines()])

                self.btn_geoloc.set_label("Envoi de la requête à Google ...")

                data = simplejson.JSONEncoder().encode(loc_req)
                try: output = simplejson.loads(urllib2.urlopen('https://www.google.com/loc/json', data).read())
                except:
                    if not self.statuGeolocLoop:
                        self.statuGeolocLoop=False
                        self.btn_geoloc.set_label("Lancer la géolocalisation")
                        self.btn_geoloc.set_sensitive(True)
                        gtk.gdk.threads_enter()
                        self.msgbox("Impossible d'envoyer la requête :\nla connexion avec l'API Google a échoué.\n\nVérifiez votre connexion internet !",1)
                        gtk.gdk.threads_leave()
                    else: self.btn_geoloc.set_label("Echec d'envoi, nouvel essai dans 5 secondes")
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

    def tabPrincipale(self):
        """Définir la page d'ouverture (TAB 1 : Accueil)"""
        self.bloc_tabs.set_current_page(1)

    def tabMenu(self):
    # Boite du menu
        boite_menu = gtk.VBox(False, 5)
        boite_menu.show()

        # Notebook du menu
        self.bloc_menu = gtk.Notebook()
        self.boite_all.pack_end(self.bloc_menu, False, False, 0)
        self.bloc_menu.set_show_tabs(0)
        self.bloc_menu.show()

        self.treestore_menu = gtk.TreeStore(str)
        self.treestore_menu.append(None, ["Accueil"])

        json_data=open(os.path.join(CONFIG_PATH, 'modules.json'))
        data = simplejson.load(json_data)
        json_data.close()

        #TODO chargement des tab via arborescence de fichier basé sur cet exemple en commentaire :
        # import unicodedata
        # import re
        for category in data.keys():
            # print re.sub(' |-|\'|/', '_', unicodedata.normalize('NFKD', unicode(category)).encode('ascii', 'ignore').lower())
            if type(data[category]) == type(list()) and len(data[category]) >= 1:
            # for module in data[category]:
            # print re.sub(' |-|\'|/', '_', unicodedata.normalize('NFKD', unicode(module['name'])).encode('ascii', 'ignore').lower())
                parent = self.treestore_menu.append(None, [category])
                [self.treestore_menu.append(parent, [module['name']]) for module in data[category]]

        self.treeview_menu = gtk.TreeView(self.treestore_menu)
        self.treeview_menu.append_column(gtk.TreeViewColumn(None, gtk.CellRendererText(), text=0))
        self.treeview_menu.set_headers_visible(False)
        self.treeview_menu.expand_all()
        self.treeview_menu.connect("cursor-changed", self.menuChoice)
        self.treeview_menu.show()

        # self.scrollbar_menu
        self.scrolled_menu = gtk.ScrolledWindow()
        self.scrolled_menu.set_placement(gtk.CORNER_TOP_RIGHT)
        self.scrolled_menu.set_size_request(self.treeview_menu.size_request()[0]+self.scrolled_menu.get_vscrollbar().size_request()[0]+5,self.treeview_menu.size_request()[1])
        self.scrolled_menu.show()
        # self.textview_menu
        self.scrolled_menu.add(self.treeview_menu)
        self.scrolled_menu.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        # Évènement qui permet de définir la largeur du menu si une scrollbar est nécessaire en fonction de la hauteur de la fenêtre
        self.fenetre.connect("size_allocate", self.onSizeAllocate)

        boite_menu.pack_start(self.scrolled_menu, True, True, 0)
        self.bloc_menu.insert_page(boite_menu, gtk.Label("Menu"), -1)

    def onSizeAllocate(self, parent, event):
        """ Permet de définir la largeur du menu si une scrollbar est nécessaire en fonction de la hauteur de la fenêtre"""
        if int(str(event).split(',')[::-1][0].lstrip().rstrip(')'))-self.fenetre.get_border_width()*2 <= self.treeview_menu.size_request()[1]+2: self.scrolled_menu.set_size_request(self.treeview_menu.size_request()[0]+self.scrolled_menu.get_vscrollbar().size_request()[0]+5,self.treeview_menu.size_request()[1])
        else: self.scrolled_menu.set_size_request(self.treeview_menu.size_request()[0]+5,self.treeview_menu.size_request()[1])

    def __init__(self):
        self.fenetre = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.fenetre.set_resizable(True)            # Autoriser le redimensionnement de la fenêtre
        self.fenetre.set_title("Free-knowledge Toolbox")    # Titre de la fenêtre
        #self.fenetre.set_decorated(False)            # Cacher les contours de la fenêtre
        self.fenetre.set_icon_from_file("%s/images/icone.png" % FKTB_PATH)    # Spécifie une icône
        self.fenetre.set_position(gtk.WIN_POS_CENTER)        # Centrer la fenêtre au lancement
        self.fenetre.set_border_width(10)            # Largueur de la bordure intérieur
        self.fenetre.set_size_request(800, 500)            # Taille de la fenêtre
        self.fenetre.connect("delete_event", self.quitDialog)    # Alerte de fermeture
        self.fenetre.connect('key-press-event', lambda o, event: event.keyval == gtk.keysyms.F11 and self.toggle_fullscreen())
        self.fenetre.show()

        self.fullscreen=0

        self.tabBuilder()        # Construction du notebook pour le contenu
        self.tabIndisp()           # Pade d'indisponibilité
        self.tabAccueil()        # Page d'accueil
        self.tabCesar()            # Page du module César
        self.tabSubstMonoAlpha()    # Page du module Substitution mono-alphabétique
        self.tabHash()            # Page du module de calcul de Hash
        self.tabmd5()            # Page du module de recherche MD5
        self.tabRegex()            # Page du module de parsage de site web
        self.tabStrings()        # Page du module de parsage de la commande strings
        self.tabMail()            # Page du module d'envoi de Mail
        self.tabASM()            # Page du module de "traduction" ASM vers "language Humain"
        self.tabCouchesRVB()        # Page du module Couches RVB (jouer avec les valeurs RVB d'une image)
        self.tabOpNot()            # Page du module Opérateur NOT
        self.tabXOR()            # Page du module de chiffrement/déchiffrement XOR
        self.tabVigenere()        # Page du module de chiffrement/déchiffrement Vigénère
        self.tabConvASCII()        # Page du module de Conversion de base : ASCII, Hexadécimal, Décimale, Octal, Binaire
        self.tabLastModif()        # Page du module d'affichage des dernières modifications éffectuées sur le disque
        self.tabGeoloc()        # Page du module de géolocalisation
        self.tabHostname()        # Page du module Hostname Resolver                            En développement
        self.tabWifi()            # Page du module Wi-Fi                                    En développement
        self.tabWifi2()            # Page du module Wi-Fi utilisant airodump-ng                        En développement
        self.tabPwdStrenght()        # Page du module de vérification de la force d'un mot de passe                En développement
        self.tabBarCode()        # Page du module de lecture / génération de code-barres                    En développement
        #self.tabCheckRFI()        # Page du module de test RFI (Remote File Inclusion)                    À venir
        #self.tabARP()            # Page du module d'ARP Poisoning                            À venir
        #self.tabHashIdentif()        # Page du module d'identification de hash                        À venir ?
        #self.tabMailAccountChecker()    # Page du module de test de compte mail                            À venir ?

        self.tabMenu()
        self.tabPrincipale()
        self.getWIface()

        gtk.main()

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.fenetre.unfullscreen()
            self.fullscreen+=1
        else:
            self.fenetre.fullscreen()
            self.fullscreen-=1

def delete():
    """Gestion des evenements de fermeture"""
    # Dès qu'on quitte : suppression des fichiers result_stega.png & result_opnot s'ils existent
    [os.remove("%s/tmp/" % FKTB_PATH + i) for i in ['result_stega.png','result_opnot', 'airodump-ng-01.csv'] if os.path.exists("%s/tmp/" % FKTB_PATH + i)]

    # TODO tuer le process airodump-ng si celui-ci est lancé via la module wifi 2
    # Vérification des permissions
    #    for su_gui_cmd in ['gksu','kdesu','ktsuss','beesu','']:
    #        if getoutput("which "+su_gui_cmd): break
    #    if not su_gui_cmd:
    #        print "Un des outils suivant est nécessaire pour acquérir les droits administrateur, veuillez en installer un :\n\ngksu\nkdesu\nktsuss\nbeesu"
    #    else: getstatusoutput(su_gui_cmd+" 'killall airodump-ng'")

    exit() # but gtk.main_quit() fail with KeyboardInterrupt ...

def main():
    # Exécution
    try:
        toolbox()
    except (KeyboardInterrupt, SystemExit):
        delete()
