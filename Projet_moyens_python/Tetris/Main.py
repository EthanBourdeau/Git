import tkinter as tk
from Game_class import Game

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bind("<KeyRelease>", self.desactivation_soft_drop)
        self.bind("<KeyPress>", self.touches_presses)
        H,W = 800,  800
        self.hauteur = 20
        self.largeur = 10
        self.creer_fen(self, H, W)
        self.config(bg='#090907')
        self.nom_piece_act = ''
        self.frame = tk.Frame(self, bg='#090907', width=W / 2, height=H)
        self.frame_sc = tk.Frame(self, bg='#090907', width=W / 2, height=H) 
        self.jeu = Game()
        self.creation_zone_score()
        self.creation_zone_jeu()
        self.creation_zone_preview_piece()
        self.frame.grid(row=0, column=0, padx=30, pady=20)
        self.frame_sc.grid(row=0, column=1)
        self.game_tic = 0
        self.soft_drop = False
        self.bja = False
        self.spda = False

    def touches_presses(self,event):
        key = event.keysym.lower()
        if key == 'q':
            self.jeu.deplacement_gauche()
            self.update_gui()
        if key == 'd':
            self.jeu.deplacement_droite()
            self.update_gui()
        if key == 'space':
            self.jeu.hard_drop()
            self.update_gui()
            self.update_gui_sec()
        if key == 's':
            self.jeu.rotation_piece()
            self.update_gui()
        if key == 'z':
            self.soft_drop = True
            self.update_gui()
        
    def desactivation_soft_drop(self,event):
        key = event.keysym.lower()
        if key == 'z':
            self.soft_drop = False

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
        for i in range(len(self.jeu.grille)):
            mid_lab = []
            for u in range(len(self.jeu.grille[i])):
                couleur = '#161614'
                lab = tk.Label(self.frame, bg=couleur)
                lab.place(x=u * (t_case + espacement), y=i * (t_case + espacement), width=t_case, height=t_case)
                mid_lab.append(lab)
            self.labels.append(mid_lab)

    def lancer_partie(self):
        if self.jeu.game_over:
            self.jeu.perdu = False
            self.jeu.game_over = False
            self.jeu.fin_lab.destroy()
            self.boucle_jeu()
        self.jeu.initialisation_variables()
        if not self.bja:
            self.boucle_jeu()
            self.bja = True
        if not self.jeu.spda:
            self.def_game_tic()
            self.jeu.spda = True
        self.jeu.ajouter_piece()

    def creation_zone_preview_piece(self):
        self.labels_sec = []
        t_case = 35
        espacement = 3
        for i in range(len(self.jeu.grille_sec)):
            mid_lab = []
            for u in range(len(self.jeu.grille_sec[i])): 
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

    def boucle_jeu(self):
        if not self.jeu.perdu:
            self.jeu.en_mouvement = True
            self.jeu.bouger_piece()
            self.jeu.suprimer_lignes_pleines(self.score_jeu, self.li_val, self.niv_val)
            self.jeu.verifier_fin()
            self.update_gui()
            self.update_gui_sec()
            self.jeu.en_mouvement = False
            self.after(self.game_tic, self.boucle_jeu)
        else :
            self.jeu.game_over = True
            self.jeu.fin_lab = tk.Label(self.frame, text="Game Over", bg='#090907', fg='white', font=('Arial', 30))
            self.jeu.fin_lab.place(x=100, y=300, height=100, width=200)
            return
    
    def update_gui(self):
        self.jeu.creer_img_fantome()
        for y in range(len(self.jeu.grille)):
            for x in range(len(self.jeu.grille[y])):
                couleur = self.jeu.grille[y][x].coul_case if self.jeu.grille[y][x].act or self.jeu.grille[y][x].transparent else '#161614'
                self.labels[y][x].config(bg=couleur)
    
    def def_game_tic(self):
        if self.soft_drop:
            self.game_tic = int(float(self.jeu.ref_frames[str(self.jeu.niv_val.get())]) * 250)
        else:
            self.game_tic = int(float(self.jeu.ref_frames[str(self.jeu.niv_val.get())]) * 2000)
        self.after(100, self.def_game_tic)
    
    def update_gui_sec(self):
        for y in range(len(self.jeu.grille_sec)):
            for x in range(len(self.jeu.grille_sec[y])):
                couleur = self.jeu.grille_sec[y][x].coul_case if self.jeu.grille_sec[y][x].act else '#161614'
                self.labels_sec[y][x].config(bg=couleur)




it = Interface()
it.mainloop()