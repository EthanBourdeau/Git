import json
import os

class Utilisateur :
    def __init__(self, n):
        self.nom = n
        self.livres_empruntés = []

    def rendre_livre (self, livre_rendre):
        self.livres_empruntés.remove(livre_rendre)

    def to_dict(self):
        return {
            "Nom_utilisateur" : self.nom,
            "Livre_empruntés": self.livres_empruntés,
            }

    def from_dict(Livre, data):
        print(data)
        return Livre([data["Nom_utilisateur"], data["Livre_empruntés"]])
        

def setup_chemins():
    chemin_absolu = os.path.abspath(__file__)
    dossier_du_fichier = os.path.dirname(chemin_absolu)
    os.chdir(dossier_du_fichier)

def recuperation_donnees_json(nom_fichier):
    setup_chemins()
    with open(f'{nom_fichier}.json', 'r', encoding='utf-8') as f:
        donnees_chargees = json.load(f)
    return donnees_chargees

def sauvegarde_donnees_json(nom_fichier, donnees_a_charger):
    setup_chemins()
    with open(f'{nom_fichier}.json', 'w', encoding='utf-8') as f:
        json.dump(donnees_a_charger, f, ensure_ascii=False, indent=4)

setup_chemins()

noms = ['Charles', 'Louis', 'Morganne', 'Tom', 'Elodie']
a = [Utilisateur(i) for i in noms]
liste_noms = [i.to_dict() for i in a]

sauvegarde_donnees_json('donnees_utilisateurs',liste_noms)
print(liste_noms)