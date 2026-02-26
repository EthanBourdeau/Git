import random
import tkinter as tk
import os
import json

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bind("<KeyRelease>", self.desactivation_soft_drop)
        self.bind("<KeyPress>", self.touches_presses)
        self.liste_pieces = self.recuperation_donnees_json('Modeles_maj.json')
        self.cols = self.recuperation_donnees_json('modeles_couleurs.json')
        self.ref_frames = self.recuperation_donnees_json('frames.json')
        H,W = 800,  800
        self.hauteur = 20
        self.largeur = 10
        self.creer_fen(self, H, W)
        self.config(bg='#090907')
        self.nom_piece_act = ''
        self.frame = tk.Frame(self, bg='#090907', width=W / 2, height=H)
        self.frame_sc = tk.Frame(self, bg='#090907', width=W / 2, height=H) 
        self.creation_zone_score()
        self.initialisation_variables()
        self.creation_zone_jeu()
        self.creation_zone_preview_piece()
        self.frame.grid(row=0, column=0, padx=30, pady=20)
        self.frame_sc.grid(row=0, column=1)
        self.bja = False
        self.spda = False

    """
    GESTION DES TOUCHES
    """

    def touches_presses(self,event):
        key = event.keysym.lower()
        if key == 'q':
            self.deplacement_gauche()
        if key == 'd':
            self.deplacement_droite()
        if key == 'space':
            self.hard_drop()
        if key == 's':
            self.rotatio_piece()
        if key == 'z':
            self.soft_drop = True

    def desactivation_soft_drop(self,event):
        key = event.keysym.lower()
        if key == 'z':
            self.soft_drop = False

    def deplacement_gauche(self):
        for y, x in self.case_act:
            c_gauche = self.grille[y][x - 1]
            if x == 0 or ([c_gauche.y, c_gauche.x] not in self.case_act) and (c_gauche.act):
                return
        for y, x in self.case_act:
            self.grille[y][x].desactiver()
        nouvelle_case_act = []
        for y, x in self.case_act:
            self.grille[y][x - 1].activer(self.cols[self.nom_piece_act])
            nouvelle_case_act.append([y, x - 1])
        self.coord_piece[1] -= 1
        self.case_act = nouvelle_case_act
        self.update_gui()

    def deplacement_droite(self):
        largeur = len(self.grille[0])
        for y, x in self.case_act:
            c_droite = self.grille[y][x + 1]
            if x == largeur - 1 or ([c_droite.y, c_droite.x] not in self.case_act) and (c_droite.act):
                return
        for y, x in self.case_act:
            self.grille[y][x].desactiver()
        nouvelle_case_act = []
        for y, x in self.case_act:
            self.grille[y][x + 1].activer(self.cols[self.nom_piece_act])
            nouvelle_case_act.append([y, x + 1])
        self.coord_piece[1] += 1
        self.case_act = nouvelle_case_act
        self.update_gui()

    def hard_drop(self): 
        while True:
            nouvelle_case_act = []
            bloquee = False
            if len(self.case_act) == 0:
                return
            for i in reversed(self.case_act):
                x = i[1]
                y = i[0]
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
            self.update_gui()

    def rotatio_piece(self):
        self.proch_index = self.index_rotation + 1
        if self.proch_index == 4:
            self.proch_index = 0
        modele_proc_piece = self.liste_pieces[self.nom_piece_act][self.proch_index]
        case_acc_maj = []
        for y,x in modele_proc_piece:
            x = x + self.coord_piece[1]
            y = y + self.coord_piece[0]
            case_acc_maj.append([y, x])
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
        self.update_gui()

    """
    SETUP DE LA FENETRE TKINTER
    """

    def creation_zone_score(self):
        self.score_jeu = tk.IntVar()
        self.lab_sc = tk.Label(self.frame_sc, textvariable=self.score_jeu, bg="#3E3E3B", fg='white', font=('Arial', 20))
        tk.Label(self.frame_sc, text = 'Score actuel',bg="#3E3E3B", fg = 'white', font=('Arial', 15)).place(x=100, y = 30)
        self.lab_sc.place(x=100, y=50, width=100, height=50)
        self.niv_val = tk.IntVar()
        self.lab_nv = tk.Label(self.frame_sc, textvariable=self.niv_val, bg="#3E3E3B", fg='white', font=('Arial', 20))
        tk.Label(self.frame_sc, text = 'Niveau de dificulté actuel',bg="#3E3E3B", fg = 'white', font=('Arial', 15)).place(x=100, y = 130)
        self.lab_nv.place(x=100, y=150, width=100, height=50)
        self.li_val = tk.IntVar()
        self.lab_li = tk.Label(self.frame_sc, textvariable=self.li_val, bg="#3E3E3B", fg='white', font=('Arial', 20))
        tk.Label(self.frame_sc, text = 'Nombre de lignes depuis le dernier niveau',bg="#3E3E3B", fg = 'white', font=('Arial', 15)).place(x=100, y = 230)
        self.lab_li.place(x=100, y=250, width=100, height=50)
        tk.Button(self.frame_sc, text='Nouvelle_partie', bg='#3E3E3B', fg='white', font=('Arial', 15), command=self.lancer_partie).place(x=100, y=700, width=200, height=40)

    def creation_zone_jeu(self):
        self.labels = []
        t_case = 35
        espacement = 3
        for i in range(len(self.grille)):
            mid_lab = []
            for u in range(len(self.grille[i])):
                couleur = '#161614'
                lab = tk.Label(self.frame, bg=couleur)
                lab.place(x=u * (t_case + espacement), y=i * (t_case + espacement), width=t_case, height=t_case)
                mid_lab.append(lab)
            self.labels.append(mid_lab)

    def creation_zone_preview_piece(self):
        self.grille_sec = [[Case(u, i) for i in range(4)] for u in range(4)]
        self.labels_sec = []
        t_case = 35
        espacement = 3
        for i in range(len(self.grille_sec)):
            mid_lab = []
            for u in range(len(self.grille_sec[i])): 
                lab = tk.Label(self.frame_sc, bg='#161614')
                lab.place(x=100+ u * (t_case + espacement), y=350 + i * (t_case + espacement), width=t_case, height=t_case)
                mid_lab.append(lab)
            self.labels_sec.append(mid_lab)

    def creer_fen(self, fen, l, h):
        screen_largeur = self.winfo_screenwidth()
        screen_hauteur = self.winfo_screenheight()
        x = (screen_largeur // 2) - (l // 2)
        y = (screen_hauteur // 2) - (h // 2)
        fen.geometry(f"{l}x{h}+{x}+{y}")
        fen.resizable(False, False)

    """
    LANCEMENT D'UNE PARTIE
    """ 
    
    def lancer_partie(self):
        if self.game_over:
            self.perdu = False
            self.game_over = False
            self.fin_lab.destroy()
            self.boucle_jeu()
        self.initialisation_variables()
        if not self.bja:
            self.boucle_jeu()
            self.bja = True
        if not self.spda:
            self.def_game_tic()
            self.spda = True
        self.update_gui()
        self.ajouter_piece()

# prpopre syst de collision ?
    def initialisation_variables(self):
        self.grille = [[Case(u, i) for i in range(self.largeur)] for u in range(self.hauteur)]
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
        self.score_jeu.set(0)
        self.niv_val.set(1)
        self.li_val.set(0)
        self.soft_drop = False

    """
    BOUCLE PERMANNTES
    """

    """
    BOUCLE : BOUCLE PRINCIPALE
    """
    def boucle_jeu(self):
        if not self.perdu:
            self.en_mouvement = True
            self.bouger_piece()
            self.suprimer_lignes_pleines()
            self.verifier_fin()
            self.update_gui()
            self.en_mouvement = False
            self.after(self.game_tic, self.boucle_jeu)
        else :
            self.game_over = True
            self.fin_lab = tk.Label(self.frame, text="Game Over", bg='#090907', fg='white', font=('Arial', 30))
            self.fin_lab.place(x=100, y=300, height=100, width=200)
            return

    def bouger_piece(self):
        nouvelle_case_act = []
        bloquee = False
        if len(self.case_act) == 0:
            return
        for y,x in reversed(self.case_act):
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
    
    def suprimer_lignes_pleines(self):
        lignes_a_s = self.verification_lignes_pleines()
        if len(lignes_a_s) != 0 :
            self.score_jeu.set(self.score_jeu.get() + 100 * 2**(len(lignes_a_s) - 1))
            for i in lignes_a_s:
                self.li_val.set(self.li_val.get() + 1)
                if self.li_val.get() == 10 :
                    self.li_val.set(0)
                    self.niv_val.set(self.niv_val.get()+ 1) 
                for u in self.grille[i]:
                    u.desactiver()
                self.descendre_grille(i)
            self.suprimer_lignes_pleines()
        else :  
            return
    
    def verification_lignes_pleines(self):
        li_a_s = []
        for y in range(len(self.grille)):
            li_a_s.append(y)
            for x in range(len(self.grille[y])) :
                if not(self.grille[y][x].act) or [y, x] in self.case_act:
                    li_a_s.pop()
                    break
        return li_a_s

    def descendre_grille(self, ligne_suprimée):
        for y in range(ligne_suprimée-1, 0, - 1):
            for x in range(len(self.grille[y])):
                 self.descendre_case(y, x)

    def descendre_case(self, y, x):
        if y < len(self.grille)- 1 and self.grille[y][x].act and not([y, x] in self.case_act) and not(self.grille[y+1][x].act):
            self.grille[y+1][x].activer(self.grille[y][x].get_col()) 
            self.grille[y][x].desactiver()
            self.descendre_case(y+1, x)  
        else:
            return 
        
    def verifier_fin(self):
        for case in self.grille[0]:
            if case.act and not ([case.y, case.x] in self.case_act):
                self.perdu = True
                break

    def update_gui(self):
        for y in range(len(self.grille)):
            for x in range(len(self.grille[y])):
                couleur = self.grille[y][x].coul_case if self.grille[y][x].act else '#161614'
                self.labels[y][x].config(bg=couleur)

    """
    BOUCLE : DEF DE LA VITESSE DE JEU
    """
    
    def def_game_tic(self):
        if self.soft_drop:
            self.game_tic = int(float(self.ref_frames[str(self.niv_val.get())]) * 250)
        else:
            self.game_tic = int(float(self.ref_frames[str(self.niv_val.get())]) * 1000)
        self.after(100, self.def_game_tic)

    """
    FIN DES BOUCLES
    """

    """
    AJOUT DE PIECE
    """

    def ajouter_piece(self):
        self.game_tic = int(float(self.ref_frames[str(self.niv_val.get())]) * 1000)
        self.actu_piece_act()
        self.update_grille_sec()
        self.update_gui_sec()
        self.index_rotation = 0
        self.coord_piece = [1, 0]
        self.case_act = list(self.liste_pieces[self.nom_piece_act][self.index_rotation])
        for y,x in self.case_act: 
            self.grille[y][x].activer(self.cols[self.nom_piece_act])
        self.update_gui()

    def actu_piece_act(self):  
        if len(self.sac_choix) == 0:
            self.sac_choix = list(self.liste_pieces.keys()) + list(self.liste_pieces.keys())
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

    def update_gui_sec(self):
        for y in range(len(self.grille_sec)):
            for x in range(len(self.grille_sec[y])):
                couleur = self.grille_sec[y][x].coul_case if self.grille_sec[y][x].act else '#161614'
                self.labels_sec[y][x].config(bg=couleur)

    """
    FCTS DE RECUP DE DONNEES JSON
    """

    def setup_chemins(self):
        chemin_absolu = os.path.abspath(__file__)
        dossier_du_fichier = os.path.dirname(chemin_absolu)
        os.chdir(dossier_du_fichier)

    def recuperation_donnees_json(self, nom_fichier):
        self.setup_chemins()
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            donnees_chargees = json.load(f)
        return donnees_chargees

class Case:
    def __init__(self, y, x):
        self.act = False
        self.x = x
        self.y = y
        self.transparent = False
        self.coul_case = 'black'

    def activer(self, c):
        self.coul_case = str(c)
        self.act = True

    def desactiver(self):
        self.act = False
    
    def act_transp(self):
        self.col = 'red'
        self.transparent = True
    
    def des_transp(self):
        self.transparent = False
    def get_col(self):
        return self.coul_case

it = Interface()
it.mainloop()