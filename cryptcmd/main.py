import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,QGridLayout, QVBoxLayout, QWidget, QPlainTextEdit, QInputDialog, QMessageBox, QListWidget, QScrollArea
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAbstractItemView
from functools import partial
from fonction import *


class MainWindow(QMainWindow):
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.setWindowTitle("Gestionnaire de mots de passe")
        self.resize(800, 600)  # Définit la taille de la fenêtre
        self.init_ui()
        self.set_styles()

    def set_styles(self):
        style = '''
            QWidget {
                background-color: #212121;
            }
            
            QLabel, QPushButton {
                color: #FFF;
            }
            
            QPushButton {
                background-color: #394b70;
                border: 1px solid #324161;
                border-radius: 5px;
                padding: 5px;
                margin: 0;
            }

            QPushButton#siteButton {
                margin-bottom: 0px;
                border-radius: 0px;
                padding: 30px;
            }
            
            QPushButton:hover {
                background-color: #404f70;
            }
            
            QPushButton:pressed {
                background-color: #4d5f87;
            }
        '''
        self.setStyleSheet(style)

    def init_ui(self):
        # Création des widgets
        self.refresh_btn = QPushButton("Rafraîchir la liste", self)
        self.add_btn = QPushButton("Ajouter un site", self)
        self.delete_btn = QPushButton("Supprimer un site", self)
        self.search_btn = QPushButton("Chercher un mot de passe", self)

        # Créer un QScrollArea pour afficher la liste des sites
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(10, 50, 280, 200)
        self.scroll_area.setWidgetResizable(True)

        self.container_widget = QWidget()
        self.scroll_area.setWidget(self.container_widget)

        self.site_layout = QGridLayout()
        self.container_widget.setLayout(self.site_layout)
        self.site_layout.setHorizontalSpacing(0)  # Assurez-vous que l'espacement horizontal est de 0
        self.site_layout.setVerticalSpacing(0)    # Assurez-vous que l'espacement vertical est de 0
        

        # Positionnement des widgets
        self.refresh_btn.setGeometry(20, 20, 200, 40)
        self.add_btn.setGeometry(20, 80, 200, 40)
        self.delete_btn.setGeometry(20, 140, 200, 40)
        self.search_btn.setGeometry(20, 200, 200, 40)
        self.scroll_area.setGeometry(240, 20, 520, 560)

        # Connexion des signaux aux slots (fonctions)
        self.refresh_btn.clicked.connect(self.refresh_liste)
        self.add_btn.clicked.connect(self.ajouter_site)
        self.delete_btn.clicked.connect(self.supprimer_mot_de_passe)
        self.search_btn.clicked.connect(self.chercher_mot_de_passe)

        # Créez les widgets pour afficher les détails du site
        self.site_label = QLabel(self)
        self.username_label = QLabel(self)
        self.password_label = QLabel(self)
        self.back_button = QPushButton("Retour", self)

        # Mise à jour de la liste des sites
        self.refresh_liste()
        # Initialisez l'affichage de la liste des sites
        self.show_site_list()


    def refresh_liste(self):
        # Supprimez tous les boutons précédemment créés
        for i in reversed(range(self.site_layout.count())):
            self.site_layout.itemAt(i).widget().setParent(None)

        liste_sites = getListeSite()
        for index, site in enumerate(liste_sites):
            site_button = QPushButton(site, self)
            site_button.setObjectName("siteButton")
            site_button.clicked.connect(partial(self.on_site_button_clicked, site))
            self.site_layout.addWidget(site_button, index, 0)  # Ajoutez le bouton à la ligne 'index' et à la colonne 0


    def on_site_button_clicked(self, site):
        try:
            d = chercher_mot_de_passe_gui(self.key, site)
            if d:
                # Affichez les détails du site et masquez la liste des sites
                self.show_site_details(site, d[0], d[1])
            else:
                QMessageBox.warning(self, "Erreur", "Aucune information trouvée pour le site : {}".format(site))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {str(e)}")



    def ajouter_site(self):
        site, ok = QInputDialog.getText(self, "Ajouter un site", "Nom du site:")
        if ok and site:
                    ajouter_mot_de_passe_gui(self.key, site)
                    self.refresh_liste()


    def chercher_mot_de_passe(self):
        site, ok = QInputDialog.getText(self, "Chercher un mot de passe", "Nom du site:")
        if ok and site:
            d = chercher_mot_de_passe_gui(self.key, site, self)
            if d:
                QMessageBox.information(self, "Informations", f"Site: {site.capitalize()}\nUsername: {d[0]}\nPassword: {d[1]}")

    def modifier_mot_de_passe(self):
        site, ok = QInputDialog.getText(self, "Modifier un mot de passe", "Nom du site:")
        if ok and site:
            modifier_mot_de_passe_gui(self.key, site, self)
            self.refresh_liste()

    def supprimer_mot_de_passe(self):
        site, ok = QInputDialog.getText(self, "Supprimer un mot de passe", "Nom du site:")
        if ok and site:
            supprimer_mot_de_passe_gui(self.key, site, self)
            self.refresh_liste()


    def show_site_details(self, site, username, password):

        # Cachez les boutons de site
        for i in range(self.site_layout.count()):
            self.site_layout.itemAt(i).widget().hide()
            
        # Créez des labels pour afficher les informations
        self.site_label = QLabel(f"Site: {site.capitalize()}", self.container_widget)
        self.username_label = QLabel(f"Username: {username}", self.container_widget)
        self.password_label = QLabel(f"Password: {password}", self.container_widget)

        # Créez un bouton pour revenir à la liste des sites
        self.back_button = QPushButton("Retour", self.container_widget)
        self.back_button.clicked.connect(self.show_site_list)

        # Ajoutez les widgets au layout
        self.site_layout.addWidget(self.site_label, 0, 0)
        self.site_layout.addWidget(self.username_label, 1, 0)
        self.site_layout.addWidget(self.password_label, 2, 0)
        self.site_layout.addWidget(self.back_button, 3, 0)

    def show_site_list(self):
        # Supprimez les widgets de détails du site
        self.site_label.setParent(None)
        self.username_label.setParent(None)
        self.password_label.setParent(None)
        self.back_button.setParent(None)

        # Affichez la liste des sites
        self.refresh_liste()



if __name__ == "__main__":
    app = QApplication([])

    key, ok = QInputDialog.getText(None, "Entrez la clé", "Clé BOZO:")
    if not ok or not key:
        sys.exit(1)

    key = key.encode('utf-8')
    key = hashlib.sha256(key).digest()

    main_window = MainWindow(key)
    main_window.show()

    sys.exit(app.exec_())
