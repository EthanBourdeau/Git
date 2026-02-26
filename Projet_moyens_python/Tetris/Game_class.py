import random
import tkinter as tk
import os
import json

class Game(tk.Tk):
    def __init__(self):
        self.fichiers_json()
        self.hauteur = 20
        self.largeur = 10 
        self.initialisation_variables()
        self.bja = False
        self.spda = False

    def fichiers_json(self):
        self.liste_pieces = self.recuperation_donnees_json('Modeles_maj.json')
        self.cols = self.recuperation_donnees_json('modeles_couleurs.json')
        self.ref_frames = self.recuperation_donnees_json('frames.json')
        

    def deplacement_gauche(self):
        for y, x in self.case_act:
            if x == 0 or ([y, x - 1] not in self.case_act) and (self.grille[y][x-1].act):
                return
        for y, x in self.case_act:
            self.grille[y][x].desactiver()
        nouvelle_case_act = []
        for y, x in self.case_act:
            self.grille[y][x - 1].activer(self.cols[self.nom_piece_act])
            nouvelle_case_act.append([y, x - 1])
        self.coord_piece[1] -= 1
        self.case_act = nouvelle_case_act
        
    def deplacement_droite(self):
        largeur = len(self.grille[0])
        for y, x in self.case_act:
            if x == largeur - 1 or ([y, x + 1] not in self.case_act) and (self.grille[y][ x + 1].act):
                return
        for y, x in self.case_act:
            self.grille[y][x].desactiver()
        nouvelle_case_act = []
        for y, x in self.case_act:
            self.grille[y][x + 1].activer(self.cols[self.nom_piece_act])
            nouvelle_case_act.append([y, x + 1])
        self.coord_piece[1] += 1
        self.case_act = nouvelle_case_act

    def hard_drop(self): 
        while True:
            nouvelle_case_act = []
            bloquee = False
            if len(self.case_act) == 0:
                return
            for y, x in reversed(self.case_act):
                position_below = [y + 1, x]
                if y + 1 >= len(self.grille) or ((position_below not in self.case_act) and (self.grille[y + 1][x].act)):
                    bloquee = True
                    break
            if bloquee:
                self.ajouter_piece()
                return
            for y, x in self.case_act:
                self.grille[y][x].desactiver()
            nouvelle_case_act = []
            for y, x in self.case_act:
                self.grille[y + 1][x].activer(self.cols[self.nom_piece_act])
                nouvelle_case_act.append([y + 1, x])
            self.coord_piece[0] += 1
            self.case_act = nouvelle_case_act
            
    def rotation_piece(self):
        self.proch_index = self.index_rotation + 1
        if self.proch_index == 4:
            self.proch_index = 0
        modele_proc_piece = self.liste_pieces[self.nom_piece_act][self.proch_index]
        case_acc_maj = []
        for y,x in modele_proc_piece:
            case_acc_maj.append([y + self.coord_piece[0], x + self.coord_piece[1]])
        peut_bouger = True
        for y,x in case_acc_maj :
            if (self.grille[y][x].act and not([y,x] in self.case_act))  or x < 0 or x >= len(self.grille[0]) or y < 0 or y >= len(self.grille):
                peut_bouger = False
        if peut_bouger:
            self.index_rotation = self.proch_index
            for y,x in self.case_act:
                self.grille[y][x].desactiver()
            self.case_act = case_acc_maj
            for y, x in self.case_act:
                self.grille[y][x].activer(self.cols[self.nom_piece_act])
        
    def initialisation_variables(self):
        self.grille = [[Case(u, i) for i in range(self.largeur)] for u in range(self.hauteur)]
        self.grille_sec = [[Case(u, i) for i in range(4)] for u in range(4)]
        self.delai = [0.8, 0.72, 0.63, 0.55, 0.47, 0.38, 0.3, 0.22, 0.13, 0.1, 0.08, 0.07, 0.05, 0.03, 0.02]
        self.sac_choix = []
        self.proch_piece = random.choice(list(self.liste_pieces.keys()))
        self.case_act = []
        self.game_over = False
        self.index_rotation = 0
        self.coord_piece = [0, 0]   
        self.case_act = []
        self.game_tic = 0
        self.perdu = False
        self.score_jeu = tk.IntVar()
        self.niv_val = tk.IntVar()
        self.niv_val.set(1)
        self.li_val = tk.IntVar()
        self.soft_drop = False

    def bouger_piece(self):
        
        nouvelle_case_act = []
        bloquee = False
        if len(self.case_act) == 0:
            return
        for y,x in reversed(self.case_act):
            position_below = [y + 1, x]
            if y + 1 >= len(self.grille) or ((position_below not in self.case_act) and (self.grille[y + 1][x].act)):
                bloquee = True
                for i in self.grille:
                    for u in i:
                        if u.transparent:
                            u.des_transp(self.cols[self.nom_piece_act])
                break
        if bloquee:
            self.ajouter_piece()
            return
        for y, x in self.case_act:
            self.grille[y][x].desactiver()
        nouvelle_case_act = []
        for y, x in self.case_act:
            self.grille[y + 1][x].activer(self.cols[self.nom_piece_act])
            nouvelle_case_act.append([y + 1, x])
        self.coord_piece[0] += 1
        self.case_act = nouvelle_case_act
    
    def ajouter_piece(self):
        self.actu_piece_act()
        self.update_grille_sec()
        self.index_rotation = 0
        self.coord_piece = [1, 0]
        self.case_act = list(self.liste_pieces[self.nom_piece_act][self.index_rotation])
        for y,x in self.case_act: 
            self.grille[y][x].activer(self.cols[self.nom_piece_act])
        
    def suprimer_lignes_pleines(self, score_jeu, li_val, niv_val):
        lignes_a_s = self.verification_lignes_pleines()
        if len(lignes_a_s) != 0 :
            score_jeu.set(score_jeu.get() + 100 * 2**(len(lignes_a_s) - 1))
            for i in lignes_a_s:
                li_val.set(li_val.get() + 1)
                if li_val.get() == 10 :
                    li_val.set(0)
                    niv_val.set(niv_val.get()+ 1) 
                for u in self.grille[i]:
                    u.desactiver()
                self.descendre_grille(i)
            self.suprimer_lignes_pleines(score_jeu, li_val, niv_val)
        else :  
            return
        
    def descendre_grille(self, ligne_suprimée):
        for y in range(ligne_suprimée-1, 0, - 1):
            for x in range(len(self.grille[y])):
                 self.descendre_case(y, x)

    def descendre_case(self, y, x):
        if y < len(self.grille)- 1 and self.grille[y][x].act and not([y, x] in self.case_act) and not(self.grille[y+1][x].act):
            self.grille[y+1][x].activer(self.grille[y][x].get_col()) 
            self.grille[y][x].desactiver()
              
        else:
            return 
        
    def verifier_fin(self):
        for case in self.grille[0]:
            if case.act and not ([case.y, case.x] in self.case_act):
                self.perdu = True
                break

    def verification_lignes_pleines(self):
        li_a_s = []
        for y in range(len(self.grille)):
            li_a_s.append(y)
            for x in range(len(self.grille[y])) :
                if not(self.grille[y][x].act) or [y, x] in self.case_act:
                    li_a_s.pop()
                    break
        return li_a_s

    def actu_piece_act(self):  
        if len(self.sac_choix) == 0:
            self.sac_choix = 2*(list(self.liste_pieces.keys()))
            random.shuffle(self.sac_choix)
        self.nom_piece_act = str(self.proch_piece)
        ind_p_p = random.randint(0, len(self.sac_choix) -1)
        self.proch_piece = self.sac_choix[ind_p_p]
        self.sac_choix.pop(ind_p_p) 
    
    def update_grille_sec(self):
        for y in range(len(self.grille_sec)):
            for x in range(len(self.grille_sec[y])):
                if [y,x] in self.liste_pieces[self.proch_piece][0]: 
                    self.grille_sec[y][x].activer(self.cols[self.proch_piece])
                else:
                    self.grille_sec[y][x].desactiver()

    def setup_chemins(self):
        chemin_absolu = os.path.abspath(__file__)
        dossier_du_fichier = os.path.dirname(chemin_absolu)
        os.chdir(dossier_du_fichier)

    def recuperation_donnees_json(self, nom_fichier):
        self.setup_chemins()
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            donnees_chargees = json.load(f)
        return donnees_chargees

    def creer_img_fantome(self):
        if len(self.case_act) == 0:
            return
        decalage = 0
        for i in self.grille:
            for u in i:
                if u.transparent:
                    u.des_transp('#161614')
        while True:
            for y, x in self.case_act:
                position_below = [y + decalage, x]
                if y + decalage >= len(self.grille) or ((position_below not in self.case_act) and (self.grille[y + decalage][x].act)):
                    self.act_transp_grille(decalage)
                    return 
            decalage += 1
        
    def act_transp_grille(self, decalage):
        
        for y, x in self.case_act:
            self.grille[y + decalage -1 ][x].act_transp()

class Case:
    def __init__(self, y, x):
        self.act = False
        self.x = x
        self.y = y
        self.transparent = False
        self.coul_case = 'black'

    def activer(self, c):
        self.coul_case = str(c)
        self.transparent = False
        self.act = True

    def desactiver(self):
        self.act = False
    
    def act_transp(self):
        self.coul_case = '#96F75E'
        self.transparent = True
    
    def des_transp(self, col):
        self.coul_case = col
        self.transparent = False

    def get_col(self):
        return self.coul_case
