from fonction import *
import colorama
from colorama import Fore, Style
import os
import getpass    
import random
from datetime import date

colorama.init()

# Fonction qui affiche l'interface
def interfaceListe():
    liste = getListeSite()
    interface = f"""
{Fore.CYAN}PASSWORD MANAGER :{Style.RESET_ALL}
    id  Titre/Service(nom)
"""

    # Calcule le nombre de colonnes
    nb_colonnes = 2
    nb_sites = len(liste)
    nb_lignes = nb_sites // nb_colonnes
    if nb_sites % nb_colonnes != 0:
        nb_lignes += 1

    # Crée une liste temporaire pour stocker les numéros et les titres
    temp_liste = []
    for i in range(nb_sites):
        num = str(i+1)
        titre = liste[i]
        temp_liste.append(num)
        temp_liste.append(titre)

    # Ajoute les numéros et les titres à l'interface en conservant la mise en forme en colonnes
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            index = i + j*nb_lignes
            if index < nb_sites:
                num = temp_liste[index*2]
                titre = temp_liste[index*2+1]
                interface += f"    {num:<4}   {titre:<25}"
        interface += "\n"

    # Ajoute les options de l'interface
    interface += f"""
{Fore.GREEN}Ajouter   Search   Modifier   Supprimer    Quitter{Style.RESET_ALL}
  [a]      [c]       [m]         [s]         [q]
"""

    print(interface)


# Fonction pour ajouter un ascii art au début du programme
def asciiart():
    h1 = Fore.GREEN + """
    
 /$$ /$$ /$$                     /$$                              
|__/| $$| $$                    |__/                              
 /$$| $$| $$  /$$$$$$   /$$$$$$  /$$  /$$$$$$  /$$   /$$  /$$$$$$ 
| $$| $$| $$ /$$__  $$ /$$__  $$| $$ /$$__  $$| $$  | $$ /$$__  $$
| $$| $$| $$| $$  \ $$| $$  \ $$| $$| $$  \ $$| $$  | $$| $$$$$$$$
| $$| $$| $$| $$  | $$| $$  | $$| $$| $$  | $$| $$  | $$| $$_____/
| $$| $$| $$|  $$$$$$/|  $$$$$$$| $$|  $$$$$$$|  $$$$$$/|  $$$$$$$
|__/|__/|__/ \______/  \____  $$|__/ \____  $$ \______/  \_______/
                       /$$  \ $$          | $$                    
                      |  $$$$$$/          | $$                    
                       \______/           |__/                    

""" + Style.RESET_ALL

    h2 = Fore.RED + """
                                         
     (   (                                   
 (   )\  )\      (  (  (     (     (     (   
 )\ ((_)((_) (   )\))( )\  ( )\   ))\   ))\  
((_) _   _   )\ ((_))\((_) )(( ) /((_) /((_) 
 (_)| | | | ((_) (()(_)(_)((_)_)(_))( (_))   
 | || | | |/ _ \/ _` | | |/ _` || || |/ -_)  
 |_||_| |_|\___/\__, | |_|\__, | \_,_|\___|  
                |___/        |_|             

""" + Style.RESET_ALL

    h3 = Fore.YELLOW + """   
 ___   ___      ___      _______  _______  ___   _______  __   __  _______ 
|   | |   |    |   |    |       ||       ||   | |       ||  | |  ||       |
|   | |   |    |   |    |   _   ||    ___||   | |   _   ||  | |  ||    ___|
|   | |   |    |   |    |  | |  ||   | __ |   | |  | |  ||  |_|  ||   |___ 
|   | |   |___ |   |___ |  |_|  ||   ||  ||   | |  |_|  ||       ||    ___|
|   | |       ||       ||       ||   |_| ||   | |      | |       ||   |___ 
|___| |_______||_______||_______||_______||___| |____||_||_______||_______|

""" + Style.RESET_ALL

    h4 = Fore.LIGHTBLUE_EX + """  
    ___       ___       ___       ___       ___       ___       ___       ___       ___   
   /\  \     /\__\     /\__\     /\  \     /\  \     /\  \     /\  \     /\__\     /\  \  
  _\:\  \   /:/  /    /:/  /    /::\  \   /::\  \   _\:\  \   /::\  \   /:/ _/_   /::\  \ 
 /\/::\__\ /:/__/    /:/__/    /:/\:\__\ /:/\:\__\ /\/::\__\  \:\:\__\ /:/_/\__\ /::\:\__\\
 \::/\/__/ \:\  \    \:\  \    \:\/:/  / \:\:\/__/ \::/\/__/   \::/  / \:\/:/  / \:\:\/  /
  \:\__\    \:\__\    \:\__\    \::/  /   \::/  /   \:\__\     /:/  /   \::/  /   \:\/  / 
   \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/  

""" + Style.RESET_ALL

    h5 = Fore.LIGHTMAGENTA_EX + """
    
██ ██      ██       ██████   ██████  ██  ██████  ██    ██ ███████ 
██ ██      ██      ██    ██ ██       ██ ██    ██ ██    ██ ██      
██ ██      ██      ██    ██ ██   ███ ██ ██    ██ ██    ██ █████   
██ ██      ██      ██    ██ ██    ██ ██ ██ ▄▄ ██ ██    ██ ██      
██ ███████ ███████  ██████   ██████  ██  ██████   ██████  ███████ 
                                            ▀▀                                                                                     
""" + Style.RESET_ALL
    #choisir aléatoirement entre les asciiart
    liste = [h1, h2, h3, h4, h5]
    return random.choice(liste)
