import random
import tkinter as tk

COLS = {
    "col_0" : "#ccc0b4",
    "col_bordure" : "#bbada0",
    "col_2" : "#efe5da",
    "col_4" : "#ecdfc9",
    "col_8" : "#f1b179",
    "col_16" : "#f69564",
    "col_32" : "#f57c61",
    "col_64" : "#f95d3e",
    "col_128" : "#ebca5f",
    "col_256" : "#ebca5f",
    "col_512" : "#ebc850",
    "col_1024" : "#ecc53e",
    "col_2048" : "#ecc02b"
}
     
class Interface (tk.Tk):
    def __init__ (self):
        super().__init__() 
        self.fen_p = tk.Toplevel(self)
        TAILLEGRILLE = self.demande_taille()
        H = 90*TAILLEGRILLE 
        W = 90*TAILLEGRILLE 
        self.creer_fen(self, H , W)
        self.size
        self.config(bg = COLS.get('col_bordure'))
        self.grille = Grille(TAILLEGRILLE)
        self.frame = tk.Frame(self, bg = COLS.get('col_bordure'))
        self.cases()
        self.frame.pack(expand= True)
        self.bind("<Key>", self.touche_pressee)
        

    def demande_taille(self):
        def aff(self):
            nonlocal result

            result = int(val.get())
            if result >= 2 and result <= 12 :
                self.fen_p.destroy()
            else : 
                self.txt.configure(text = 'Veuillez choisir une valeur valable')

        self.creer_fen(self.fen_p, 300, 100)
        self.fen_p.title("Choix de la taille")
        self.txt = tk.Label(self.fen_p, text='Entrez une valeur entre 2 et 12')
        self.txt.pack(pady = 10)
        val = tk.StringVar()
        tk.Entry(self.fen_p, textvariable=val).pack()
        tk.Button(self.fen_p, text='Valider', command=lambda : aff(self)).pack(pady = 10)
        result = None
        self.fen_p.wait_window()  # Attend que la fenêtre soit fermée
        return result

    def cases (self):
        self.labels = []
        for i in range (len(self.grille.grille)):
            mid_lab = []
            for u in range (len(self.grille.grille[i])):
                case = self.grille.grille[i][u]
                col = COLS.get(f'col_{case.valeur}')
                lab = tk.Label(self.frame, bg = col, width=11, height=5, text=case.valeur if case.valeur != 0 else ' ')
                mid_lab.append(lab)
                lab.grid(pady = 2, padx = 2,column=u, row=i)
            self.labels.append(mid_lab)

    def touche_pressee(self, event):
        if event.keysym == "z":
            self.tour_suiv('z')

        elif event.keysym == "s":
            self.tour_suiv('s')

        elif event.keysym == "q":
            self.tour_suiv('q')

        elif event.keysym == "d":
            self.tour_suiv('d')

    def tour_suiv(self, t):
        self.bouger(t)
        self.ajouter_case()
        self.maj_grille()

    def maj_grille(self):
        for i in range(len(self.labels)):
            for u in range(len(self.labels[i])):
                c = self.grille.grille[i][u]
                lab = self.labels[u][i]
                col = COLS.get(f'col_{c.valeur}')
                lab.config(bg=col, text=c.valeur if c.valeur != 0 else ' ')

    def aff(self):
        print(' ')
        for i in range(len(self.grille.grille)) :
            for u in range(len(self.grille.grille[i])) :
                print(self.grille.grille[i][u].valeur, end = '')
            print()

    def bouger(self, dir):
        ancien_liste = []
        while True:
            self.liste_act = []
            p1 = {  'q': range(len(self.grille.grille)),
                    'z': range(len(self.grille.grille)),
                    's' : reversed(range(len(self.grille.grille))),
                    'd' : reversed(range(len(self.grille.grille)))          
                    }
            for i in p1[dir] :
                p2 = {  'q': range(len(self.grille.grille[i])),
                    'z': range(len(self.grille.grille[i])),
                    's' : reversed(range(len(self.grille.grille[i]))),
                    'd' : reversed(range(len(self.grille.grille[i])))          
                    }
                for u in p2[dir] :
                    dic = { 'z':[ u > 0                            , i      , u - 1 ], 
                            's':[ u < len(self.grille.grille) - 1  , i      , u + 1 ], 
                            'q':[ i > 0                            , i - 1  , u     ], 
                            'd':[ i < len(self.grille.grille) - 1  , i + 1  , u     ]
                               }
                    if  dic[dir][0]   :
                        if self.grille.grille[i][u].remplis and not(self.grille.grille[dic[dir][1]][dic[dir][2]].remplis) :
                            self.liste_act.append([i, u])
                            self.grille.grille[dic[dir][1]][dic[dir][2]].affect_valeur(self.grille.grille[i][u].valeur)
                            self.grille.grille[i][u].retirer_valeur()
                        elif self.grille.grille[dic[dir][1]][dic[dir][2]].valeur == self.grille.grille[i][u].valeur and self.grille.grille[i][u].valeur != 0:
                            self.grille.grille[dic[dir][1]][dic[dir][2]].affect_valeur(self.grille.grille[i][u].valeur * 2)
                            self.grille.grille[i][u].retirer_valeur()
            if ancien_liste == self.liste_act:
                break   
            ancien_liste = self.liste_act

    def ajouter_case(self):
        empty_cases = [case for row in self.grille.grille for case in row if not case.remplis]
        if len( empty_cases) == 0:
            self.destroy()
        n_case = random.choice(empty_cases)
        n_case.affect_valeur(random.choice((2, 4)))
        self.labels[n_case.x][n_case.y].config(bg = COLS.get(f'col_{n_case.valeur}'), text = n_case.valeur)

    def fin_jeu (self): 
        self.quit()

    def creer_fen (self, fen, l, h):
        screen_largeur = self.winfo_screenwidth()
        screen_hauteur = self.winfo_screenheight()
        x = (screen_largeur // 2) - (l // 2)
        y = (screen_hauteur // 2) - (h // 2)
        fen.geometry(f"{l}x{h}+{x}+{y}") # Definit la taille de la fenetre et empeche sa modification
        fen.resizable(False, False)     
    

class Grille :
    def __init__(self, taille):
        self.grille = [[Case(0, u, i) for i in range (taille)]for u in range (taille)]
        
        for i in range (6):
            a = random.choice (self.grille[random.randint(0, len(self.grille) - 1)])
            a.affect_valeur(random.choice((2, 4)))


class Case :
    def __init__(self, valeur, x, y):
        self.x = x
        self.y = y
        self.remplis = False
        if valeur > 0 :
            self.affect_valeur(valeur)
        else:
            self.valeur = 0

    def affect_valeur(self, valeur):
        self.valeur = valeur
        self.remplis = True
    
    def retirer_valeur (self):
        self.valeur = 0
        self.remplis = False

it = Interface()
it.mainloop()





