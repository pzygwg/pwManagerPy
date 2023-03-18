import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import getpass
import random
import string
from io import UnsupportedOperation
from PySide2.QtWidgets import QInputDialog, QMessageBox


# Fonction pour créer une clé à partir d'un mot de passe
def creer_cle(mdp):
    sel = b'\xc8\x8f\xf9\xc5Z\xeb\xf7N\xaf\xd8$\xd7\xae@\x17\xdb'
    key = hashlib.pbkdf2_hmac('sha256', mdp.encode(), sel, 100000)
    return key

# Fonction pour générer un vecteur d'initialisation (IV)
def generate_iv():
    return os.urandom(16)

# Fonction pour crypter un message
def crypter(message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(message) + encryptor.finalize()
    return ct

# Fonction pour décrypter un message
def decrypter(ct, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    d = decryptor.update(ct) + decryptor.finalize()
    return d.rstrip(b'\0')


# Fonction pour ajouter un mot de passe avec interface graphique
def ajouter_mot_de_passe_gui(key, site, parent=None):
    site = site.lower()
    filename = f"{site}.txt"
    if os.path.isfile(filename):
        QMessageBox.warning(parent, "Erreur", "Ce site existe déjà.")
        return

    username, ok = QInputDialog.getText(parent, "Ajouter un mot de passe", "Nom d'utilisateur:")
    if not ok or not username:
        return

    password, ok = QInputDialog.getText(parent, "Ajouter un mot de passe", "Mot de passe:")
    if not ok or not password:
        return

    iv = generate_iv()
    data = f"{username}: {password}"
    data = data.encode('utf-8')
    data += b'\0' * (16 - len(data) % 16)
    ct = crypter(data, key, iv)
    with open(filename, 'wb') as file:
        file.write(iv)
        file.write(ct)

    QMessageBox.information(parent, "Succès", "Mot de passe ajouté avec succès.")

# ... (inclusion des autres fonctions modifiées)

# Fonction pour avoir la liste des sites
def getListeSite():
    liste = []
    for file_name in os.listdir():
        if file_name.endswith('.txt'):
            site = file_name[:-4].capitalize()
            liste.append(site)
    return liste


# Fonction pour chercher un mot de passe avec interface graphique
def chercher_mot_de_passe_gui(key, site, parent=None):
    site = site.lower()
    filename = f"{site}.txt"

    try:
        with open(filename, 'rb') as file:
            iv = file.read(16)
            ct = file.read()
    except FileNotFoundError:
        QMessageBox.warning(parent, "Erreur", "MDP non trouvé ou mauvaise clé BOZO")
        return None

    try:
        d = decrypter(ct, key, iv).decode('utf-8')
    except ValueError:
        QMessageBox.warning(parent, "Erreur", "MDP non trouvé ou mauvaise clé BOZO")
        return None

    d = d.split(': ')
    if len(d) != 2:
        QMessageBox.warning(parent, "Erreur", "Erreur lors de la récupération des informations du site.")
        return None

    return d




# Fonction pour modifier un mot de passe avec interface graphique
def modifier_mot_de_passe_gui(key, site, parent=None):
    site = site.lower()
    filename = f"{site}.txt"

    try:
        with open(filename, 'rb') as file:
            iv = file.read(16)
            ct = file.read()
    except FileNotFoundError:
        QMessageBox.warning(parent, "Erreur", "MDP non trouvé ou mauvaise clé BOZO")
        return

    try:
        d = decrypter(ct, key, iv).decode('utf-8')
    except ValueError:
        QMessageBox.warning(parent, "Erreur", "MDP non trouvé ou mauvaise clé BOZO")
        return

    d = d.split(': ')
    username, ok = QInputDialog.getText(parent, "Modifier un mot de passe", "Nouveau nom d'utilisateur:", text=d[0])
    if not ok or not username:
        return

    password, ok = QInputDialog.getText(parent, "Modifier un mot de passe", "Nouveau mot de passe:", text=d[1])
    if not ok or not password:
        return

    data = f"{username}: {password}"
    data = data.encode('utf-8')
    data += b'\0' * (16 - len(data) % 16)
    ct = crypter(data, key, iv)
    with open(filename, 'wb') as file:
        file.write(iv)
        file.write(ct)

    QMessageBox.information(parent, "Succès", "Mot de passe modifié avec succès.")


# Fonction pour supprimer un mot de passe avec interface graphique
def supprimer_mot_de_passe_gui(key, site, parent=None):
    site = site.lower()
    filename = f"{site}.txt"

    try:
        with open(filename, 'rb') as file:
            iv = file.read(16)
            ct = file.read()
    except FileNotFoundError:
        QMessageBox.warning(parent, "Erreur", "Pas la bonne clé BOZO")
        return

    try:
        _ = decrypter(ct, key, iv).decode('utf-8')
    except ValueError:
        QMessageBox.warning(parent, "Erreur", "Pas la bonne clé BOZO")
        return

    reply = QMessageBox.question(parent, "Supprimer", f"Voulez-vous vraiment supprimer le site {site.capitalize()}?", QMessageBox.Yes | QMessageBox.No)

    if reply == QMessageBox.Yes:
        os.remove(filename)
        QMessageBox.information(parent, "Succès", "Site supprimé.")
    
