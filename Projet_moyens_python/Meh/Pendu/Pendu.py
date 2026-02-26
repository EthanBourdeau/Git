import os
import json    
import random

class Pendu:
    def __init__(self):
        liste_mots =self.recuperation_donnees_json('mots.json')
        self.mot_choisi = random.choice(liste_mots)
        self.lettres_données = []
        self.lettres_a_trouver = []
        self.essais_restants = 8
        for lettre in self.mot_choisi:
            if lettre not in self.lettres_a_trouver:
                self.lettres_a_trouver.append(lettre)
        self.boucle_jeu()
    

    def setup_chemins(self):
        chemin_absolu = os.path.abspath(__file__)
        dossier_du_fichier = os.path.dirname(chemin_absolu)
        os.chdir(dossier_du_fichier)

    def recuperation_donnees_json(self, nom_fichier):
        self.setup_chemins()
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            donnees_chargees = json.load(f)
        return donnees_chargees

    def demander_lettre(self):
        lettre_rentree = input("Rentre une nouvelle lettre :")
        print(lettre_rentree)
        if lettre_rentree in self.lettres_a_trouver:
            self.lettres_données.append(lettre_rentree)
        else:
            print('mauvaise lettre')
            self.lettres_données.append(lettre_rentree)
            self.essais_restants-= 1


    def verifier_victoire(self):
        for lettre in self.lettres_a_trouver:
                if lettre not in self.lettres_données:
                    return False
        return True

    def affiche_mot(self):
        for i in self.lettres_a_trouver:
            if i in self.lettres_données:
                print(i, end = "")
            else :
                print(' _', end ="")
        print()
        print(f'Vies restatntes {self.essais_restants}')
        print('Lettres deja données :', end = "")
        for i in self.lettres_données:
            print(i, end =" ")
        print()

    def boucle_jeu(self):
        while True :
            if self.essais_restants < 1:
                print('perdu')
                print(f'Le mot a trouver etait {self.mot_choisi}')
                break
            elif self.verifier_victoire():
                print('vous avez gagné')
                break
            else:
                self.affiche_mot()
                self.demander_lettre()        
            



P = Pendu()