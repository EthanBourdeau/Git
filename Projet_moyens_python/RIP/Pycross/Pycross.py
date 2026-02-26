import tkinter as tk 
import random as rd
import time as t

class Interface (tk.Tk):
    def __init__ (self):
        super().__init__()
        self.title("Jeu de rythme quelconque")
        self.fen_p = tk.Toplevel(self)
        TAILLEGRILLE = self.demande_taille()
        H = 54*(TAILLEGRILLE)
        W = 52*(TAILLEGRILLE + 1)
        self.grille = Grille(TAILLEGRILLE)
        self.creer_fen(self, H , W)
        self.frame = tk.Frame(self, height= H, width= W,  bg = 'white')
        self.cases()
        tk.Button(self, text = 'Lancement du jeu', command = self.clignote_aleatoire).pack(pady = 5)    
        self.frame.pack(padx= 10, pady= 10)
        self.frame.pack_propagate(False)

    def victoire (self):
        fen_vic = tk.Toplevel(self)
        self.creer_fen(fen_vic, 200, 100)
        self.frame_victoire = tk.Frame(fen_vic, height= 100, width= 200,  bg = 'white')
        tk.Label(self.frame_victoire, text = 'Victoire !').pack(pady = 20)
        self.frame_victoire.pack(padx= 10, pady= 10)
        self.frame_victoire.pack_propagate(False)
        self.after(2000, self.destroy)

    def clignote_aleatoire(self):
        duree = 1000
        for i in range(self.grille.taille ** 2):
            case = self.grille.choix_case()
            case.activer(i )
            bouton = self.labels[case.x][case.y]
            print(case.x, case.y)
            self.after(i * duree, lambda  b = bouton  :self.clignoter(b))
            
        
        """
        if self.grille.cases_disponibles():
            case = self.choix_case(self.grille.grille[rd.randint(0, len(self.grille.grille)- 1)][rd.randint(0, len(self.grille.grille)- 1)])
            case.activer()
            bouton = self.labels[case.x][case.y]
            print(case.x, case.y)
            self.clignoter(bouton, case)
        else :
            self.victoire()
        """
        
    def choix_case(self, case):
        if case.cli:
            return self.choix_case(self.grille.grille[rd.randint(0, len(self.grille.grille) - 1)][rd.randint(0, len(self.grille.grille )- 1)])
        else:
            return case
        
    def clignoter(self, le_bouton):
        le_bouton.config(bg = 'green')
        self.after(1000, lambda: le_bouton.config(bg = 'white'))

    def cases(self):
        self.labels = []
        taille_case = 45
        espacement = 5
        for i in range(len(self.grille.grille)):
            mid_lab = []
            for u in range(len(self.grille.grille[i])):
                case = self.grille.grille[i][u]
                couleur = 'white'
                # Cadre noir (bordure)
                cadre = tk.Frame(self.frame, bg='black',
                                width=taille_case + 2,
                                height=taille_case + 2
                                )
                x = u * (taille_case + espacement)
                y = i * (taille_case + espacement)
                cadre.place(x=x, y=y)

                # Case intérieure
                lab = tk.Button(cadre, bg=couleur, relief = 'flat')
                lab.place(x=1, y=1, width=taille_case, height=taille_case)
                mid_lab.append(lab)
            self.labels.append(mid_lab)

    def demande_taille(self):
        def aff(self):
            nonlocal result
            result = int(val.get())
            if result >= 3 and result <= 15 :
                self.fen_p.destroy() 
            else : 
                self.txt.configure(text = 'Veuillez choisir une valeur valable')


        self.creer_fen(self.fen_p, 300, 100)
        self.fen_p.title("Choix de la taille")
        self.txt = tk.Label(self.fen_p, text='Entrez une valeur entre 3 et 12')
        self.txt.pack(pady = 10)
        val = tk.StringVar()
        tk.Entry(self.fen_p, textvariable=val).pack()
        tk.Button(self.fen_p, text='Valider', command=lambda : aff(self)).pack(pady = 10)

        result = None
        self.fen_p.wait_window()  # Attend que la fenêtre soit fermée
        return result
    
    def creer_fen (self, fen, l, h):
        screen_largeur = self.winfo_screenwidth()
        screen_hauteur = self.winfo_screenheight()
        x = (screen_largeur // 2) - (l // 2)
        y = (screen_hauteur // 2) - (h // 2)
        fen.geometry(f"{l}x{h}+{x}+{y}") # Definit la taille de la fenetre et empeche sa modification
        fen.resizable(False, False)  

class Case ():
    def __init__(self, x, y):
        self.cli = False
        self.rang = 0
        self.x = x
        self.y = y
    
    def activer(self, rang):
        self.cli = True
        self.rang = rang

class Grille():
    def __init__(self, t):
        self.taille = t
        self.grille = []
        self.crea_grille(self.taille)

    def cases_disponibles(self):
        for i in self.grille:
            for u in i:
                if not u.cli:
                    return True
        return False
    def crea_grille(self, t):
        self.grille = [[Case(i, u) for u in range (t)] for i in range(t)]
    
    def choix_case(self):
        rand = rd.choice(self.grille[rd.randint(0, self.taille - 1)])  
        if rand.cli :
            return self.choix_case()
        else :
            return rand

    def __str__(self):
        for i in self.grille:
            for u in i:
                print(u.col, end = "")
            print()
        return '\nGrille actuelle'

it = Interface()
it.mainloop()
