import tkinter as tk
import random 

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        H, W = 1200,  800
        self.hauteur_grille = 15
        self.largeur_grille = 15
        self.bind("<KeyPress>", self.touches_presses)
        self.creer_fen(self, H, W)
        self.config(bg = 'green')
        self.frame_g = tk.Frame(self, width=800, height=H, bg="black")
        self.frame_sc = tk.Frame(self, bg='#090907', width=400, height=H)
        self.creation_zone_score()
        self.initialisation_variables()
        self.creation_zone_jeu() 
        self.frame_g.grid(row = 0, column = 0)
        self.frame_sc.grid(row = 0, column = 1)
        self.bja = False
        self.spda = False
        self.c_serpent = []
    
    def touches_presses(self,event):
        key = event.keysym.lower()
        if key == 'q' and self.orientation!= [0, 1]:
            self.orientation = [0, -1]
            self.update_gui()
        elif key == 'd' and self.orientation != [0, -1]:
            self.orientation = [0, 1]
            self.update_gui()
        elif key == 's' and self.orientation != [-1, 0]:
            self.orientation = [1, 0]
            self.update_gui()
        elif key == 'z'and self.orientation != [1, 0]:
            self.orientation = [-1, 0]
            self.update_gui()

    def lancer_partie(self):
        if self.game_over:
            self.perdu = False
            self.game_over = False
            self.boucle_jeu()
        self.initialisation_variables()
        if not self.bja:
            self.boucle_jeu()
            self.bja = True
        try:
            self.fin_lab.destroy()
        except:
            pass
        self.update_gui()
        
    def boucle_jeu(self):
        print(self.game_tic)
        if not self.perdu:
            self.avancer_serpent()
            self.update_gui()
            self.after(self.game_tic, self.boucle_jeu)
        else :  
            self.fin_lab = tk.Label(self, text="Game Over", bg='#090907', fg='white', font=('Arial', 30))
            self.fin_lab.place(x=100, y=300, height=100, width=200)
            return

    def reduire_game_tic(self):
        self.game_tic = int(self.game_tic * 0.97)
        

    def verifier_fin(self):
        proch_pos = [self.c_serpent[0][0] + self.orientation[0], self.c_serpent[0][1] + self.orientation[1]]
        for i in proch_pos:
            if i < 0 or i > (len(self.grille.grille) - 1):
                self.perdu = True 
                self.game_over= True 
                return True
        if proch_pos in self.c_serpent:
            self.perdu = True 
            self.game_over= True 
            return True
        return False
    
    def avancer_serpent(self):
        if self.verifier_fin():
            print('fin')     
        else:
            proch_pos = [self.c_serpent[0][0] + self.orientation[0], self.c_serpent[0][1] + self.orientation[1]]
            if proch_pos == self.pomme:
                self.score_jeu.set(self.score_jeu.get()+ 1)
                self.reduire_game_tic() 
                self.bouger_pomme()
            self.c_serpent.pop()
            self.c_serpent.insert(0, proch_pos)

    def bouger_pomme(self):
        nouv_pos = [random.randint(0, len(self.grille.grille) - 1), random.randint(0, len(self.grille.grille) - 1)]
        if nouv_pos in self.c_serpent or nouv_pos == self.pomme:
            self.bouger_pomme()
        else :
            self.c_serpent.insert(0, [self.c_serpent[0][0] + self.orientation[0], self.c_serpent[0][1] + self.orientation[1]])
            self.pomme = nouv_pos

    def update_gui(self):
        self.vit_ac.set(round((1/ (self.game_tic / 1000)), 2))
        for y in range(len(self.grille.grille)):
            for x in range(len(self.grille.grille[y])):
                couleur = self.grille.grille[y][x]
                self.labels[y][x].config(bg=couleur)  
        for y,x in self.c_serpent :
            self.labels[y][x].config(bg = 'blue')
        self.labels[self.pomme[0]][self.pomme[1]].config(bg = 'red')

    def initialisation_variables(self):
        self.grille = Grille(self.hauteur_grille, self.largeur_grille)
        self.c_serpent = [[self.hauteur_grille // 2,(self.largeur_grille // 2) +1 ],
                          [self.hauteur_grille // 2,self.largeur_grille // 2 ], 
                          [self.hauteur_grille // 2,(self.largeur_grille // 2 )- 1 ]]
        self.game_over = False
        self.perdu = False
        self.pomme = [0, 0]
        self.orientation = [0,1]
        self.bouger_pomme()
        self.game_tic = 300
        self.score_jeu.set(0)
        self.vit_ac.set(0)
        self.li_val.set(0)
        
    
    def creer_fen(self, fen, l, h):
        screen_largeur = self.winfo_screenwidth()
        screen_hauteur = self.winfo_screenheight()
        x = (screen_largeur // 2) - (l // 2)
        y = (screen_hauteur // 2) - (h // 2)
        fen.geometry(f"{l}x{h}+{x}+{y}")
        fen.resizable(False, False)

    def creation_zone_score(self):
        self.score_jeu = tk.IntVar()
        self.lab_sc = tk.Label(self.frame_sc, textvariable=self.score_jeu, bg="#3E3E3B", fg='white', font=('Arial', 20))
        tk.Label(self.frame_sc, text = 'Score actuel',bg="#3E3E3B", fg = 'white', font=('Arial', 15)).place(x=100, y = 30)
        self.lab_sc.place(x=100, y=50, width=100, height=50)
        self.vit_ac = tk.IntVar()
        self.lab_nv = tk.Label(self.frame_sc, textvariable=self.vit_ac, bg="#3E3E3B", fg='white', font=('Arial', 20))
        tk.Label(self.frame_sc, text = 'Vitesse actuelle (cases / minutes)',bg="#3E3E3B", fg = 'white', font=('Arial', 15)).place(x=100, y = 130)
        self.lab_nv.place(x=100, y=150, width=100, height=50)
        self.li_val = tk.IntVar()
        self.lab_li = tk.Label(self.frame_sc, textvariable=self.li_val, bg="#3E3E3B", fg='white', font=('Arial', 20))
        tk.Label(self.frame_sc, text = 'Nombre de lignes depuis le dernier niveau',bg="#3E3E3B", fg = 'white', font=('Arial', 15)).place(x=100, y = 230)
        self.lab_li.place(x=100, y=250, width=100, height=50)
        tk.Button(self.frame_sc, text='Nouvelle_partie', bg='#3E3E3B', fg='white', font=('Arial', 15), command=self.lancer_partie).place(x=100, y=700, width=200, height=40)


    def creation_zone_jeu(self):
        self.labels = []
        t_case = 800 // self.hauteur_grille
        for i in range(self.hauteur_grille):
            mid_lab = []
            for j in range(self.largeur_grille):
                case = tk.Label(self.frame_g, bg=self.grille.grille[i][j], width=4, height=2, borderwidth=0, relief="solid")
                case.place(y = i* t_case, x = j*t_case,width=t_case, height=t_case)
                mid_lab.append(case)
            self.labels.append(mid_lab)



class Grille:
    def __init__(self, hauteur, largeur):
        self.hauteur = hauteur
        self.largeur = largeur
        self.grille = []
        self.remplir_grille()
        
    def remplir_grille(self):
        for i in range(self.hauteur):
            g_t = []
            for j in range(self.largeur):
                if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                    col = '#aad751'
                else :
                    col = '#a2d149'
                g_t.append(col)
            self.grille.append(g_t)

    def afficher_grille(self):
        for ligne in self.grille:
            print(ligne)

it = Interface()
it.mainloop()