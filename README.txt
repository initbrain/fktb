FREE-KNOWLEDGE TOOLBOX
GNU General Public License v3.0 - http://www.gnu.org/licenses/gpl-3.0.txt

Modifications du 20/06/2012 (v0.2.3) :
	- Correction (fautes d'orthographe)
	- Ajout d'un nouveau contributeur
	- Correction d'un problème avec le chemin d'accès au dossier "images"
	- Correction d'une erreur dans le module de chiffrement XOR
	- Optimisation du code, correction d'une erreur avec la prise en compte
	  des espaces et gestion de tout les autres caractères d'espacement
	  dans le module de chiffrement Vigenère
	- Amélioration de la vérification des mises à jour
	- Ajout d'un module de substitution mono-alphabétique
	- Refonte totale de l'interface graphique pour la rendre maximisable
	- Correction d'un problème de transparence avec les images affichées
	- Possibilité de modifier la date dans l'entête dans le module Mail "Anonyme"
	- Affichage du nombre de résultats dans le module "Commande strings"
	- Modification du module de Chiffrement XOR :
	  Possibilité de saisir l'entrée en ASCII ou en Décimal
	  et d'afficher le résultat dans un de ces deux formats
	- Modification du module de Traduction ASM :
	  Affichage des résultats dans une listview
	  Gestion des erreurs de saisie
	- Amélioration du menu :
 	  Affichage par catégories
	  Modification de la largueur pour correspondre à différente taille de police
	  Ajout d'une scrollbar verticale
	  Utilisation d'un évènement qui permet de définir la largueur si une scrollbar
	  est nécessaire en fonction de la hauteur de la fenetre principale
	- Ajout d'un module permettant d'afficher la liste des points d'accès WiFi
	  présents aux alentours ainsi que leur signal
	- Module de convertion de base (ASCII, Hexadécimal, Décimal, Octal, Binaire)
	- Ajout d'un module permettant de calculer la "force" d'un mot de passe
	- Possibilité de mettre en plein écran avec la touche F11
	- Nouveau logo sur la page d'accueil
	- Module de monitoring de fichier
	- Module permettant de connaitre les hostnames enregistrés sur le réseau
	- Module de géolocalisation (Wifi Positioning System)
	- Ajout d'un module dans la catégorie crypto : Opérateur NOT
	- Ajout d'un dossier temporaire (tmp)

Modifications du 08/11/2011 (v0.2.2) :
	- Ajout de deux modules de chiffrement/déchiffrement : XOR et Vigenère
	- Mise à jour du module de recherche MD5

Modifications du 23/08/2011 (v0.2.1) :
	- Modification du design de la fenêtre "À Propos"

Modifications du 22/08/2011 (v0.2.0) :
	- Modification du menu pour une meilleure lisibilité
	- Modification des méthodes de notification
	- Modification de l'aide pour les regex

Modifications du 07/08/2011 (v0.1.9) :
	- Ajout d'un module de stéganographie (cacher et lire du texte dans les valeurs RVB d'une image)
	- Meilleur détermination du chemin d'accès au dossier "images"
	- Modification de la fenêtre "À Propos"
	  nouvelle adresse email de contact
	  modification du lien vers le site internet
	- Bouton sur la page d'accueil pour vérifier les mises à jour

Modifications du 02/07/2011 (v0.1.8) :
	- Réorganisation du code source
	- Ajout d'un module "Hash" pour calculer le hash md5, sha1,
	  sha224, sha256, sha384 ou sha512 d'un texte ou d'un fichier

Modifications du 13/06/2011 (v0.1.7) :
	- Changement du nom de la toolbox
	- Correction (fautes d'orthographe)

Modifications du 19/05/2011 (v0.1.6) :
	- Ajout de notifications partie MD5 et Mail
	- Modification de la position d'ouverture de certaine fenêtre
	- Ajout d'un module "ASM" pour désassembler/traduire un binaire en "langage humain"

Modifications du 04/05/2011 (v0.1.5) :
	- Implémentation de la fonction de décryptage dans le module César

Modifications du 01/05/2011 (v0.1.4) :
	- Gestion threadée des recherches MD5 en ligne
	- Ajout d'une barre de progression dans le module MD5
	- Gestion du cas où un site serait hors-ligne
	- Ajout d'un module de mail-bombing
	  avec possibilité d'envoyer une pièce-jointe

Modifications du 17/04/2011 (v0.1.3) :
	- Modification de la fenêtre "À Propos"
	  ajout des contributeurs
	  lien vers mon site : http://www.initbrain.fr
	- Ajout du module Strings (avec usage de regex facultatif)
	- Suppression des scrollbars de l'aide regex
	- Ajout d'un fond sympa sur l'onglet d'accueil

Modifications du 16/04/2011 (v0.1.2) :
	- Corréction d'un problème dans les scripts de chiffrement / déchiffrement César
	- Modification de l'agencement des widgets dans le module César
	- Ajout d'un aide minimale dans le module Regex
	- Modification de l'agencement des widgets dans le module Regex
	- Ajout du logo de licence GNU/GLP v3 dans la fenêtre "À Propos ..."
	- Modification de l'icône de l'application

Modifications du 16/04/2011 (v0.1.1) :
	- Augmentation de la taille générale de la toolbox
	- Alignement à gauche du texte de tout les labels
	- Ajout d'un logo de soutient à l'April (avec lien vers le site http://www.april.org)
	- Déplacement du boutton "À Propos" en haut a droite sur la page d'accueil
	- Agrandissement des fenêtres interdit (à voir si on garde :
	  projet d'adaptation des résultats en plein écran)
	- Gestion des majuscules dans le module César

À venir :
	- Gestion des modules avec possibilité de vérifier les mises à jour au lancement
	- Vérification des importations et désactivation de certains modules en fonction de ça
	- Création du module MAC to IP (retrouver une adresse IP à partir d'une adresse MAC)
	- Création du module hack switch (ARP Flooding)
	- Ajout d'un fichier de préférence pour :
	  mettre par défaut du contenu dans les champs
	  autoriser les mises à jour automatiques
	- Gestion multilingue
	- Mettre en place une vérification de tout les champs de saisie
	- Créer d'autres modules de chiffrement
	- Module ARP Poisoning avec ou sans redirection de trafic
	  Avec demande du mot de passe root à partir du moment où on lui passe en paramètre
	  ce dont'il a besoin pour faire l'ARP Poisoning
	- Module de récupération de fichiers supprimés
	  dans image disque / périphérique amovible / disque dur
	- Module comme pour md5 mais avec sha1
	- Module de chiffrement personnalisable avec
	  rotation alphabétique, clé de chiffrement à la Vigenère,
	  salage positionnable et peut-être même un petit coup de XOR au choix
	- Module Carré de polybe
	- Module de test de buffer overflow (fuzzing des arguments)
