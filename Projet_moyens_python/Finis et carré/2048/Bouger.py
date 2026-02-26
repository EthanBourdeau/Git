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


def mouv(self, dir):
    ancien_liste = []
    while True:
        self.liste_act = []
        for i in range(len(self.grille.grille)) :
            for u in range(len(self.grille.grille[i])) :
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
    
def bas(self):
    ancien_liste = []
    while True:
        self.liste_act = []
        for i in range(len(self.grille.grille)) :
            for u in range(len(self.grille.grille[i])) :
                if  u < len(self.grille.grille) - 1   :
                    if self.grille.grille[i][u].remplis and not(self.grille.grille[i][u + 1].remplis) :
                        self.liste_act.append([i, u])
                        self.grille.grille[i][u + 1].affect_valeur(self.grille.grille[i][u].valeur)
                        self.grille.grille[i][u].retirer_valeur()
                    elif self.grille.grille[i][u + 1].valeur == self.grille.grille[i][u].valeur and self.grille.grille[i][u].valeur != 0:
                        self.grille.grille[i][u + 1].affect_valeur(self.grille.grille[i][u].valeur * 2)
                        self.grille.grille[i][u].retirer_valeur()
        if ancien_liste == self.liste_act:
            break
        ancien_liste = self.liste_act

def haut(self):
    ancien_liste = []
    while True:
        self.liste_act = []
        for i in range(len(self.grille.grille)) :
            for u in range(len(self.grille.grille[i])) :
                if  u > 0   :
                    if self.grille.grille[i][u].remplis and not(self.grille.grille[i][u - 1].remplis) :
                        self.liste_act.append([i, u])
                        self.grille.grille[i][u - 1].affect_valeur(self.grille.grille[i][u].valeur)
                        self.grille.grille[i][u].retirer_valeur()
                    elif self.grille.grille[i][u - 1].valeur == self.grille.grille[i][u].valeur and self.grille.grille[i][u].valeur != 0:
                        self.grille.grille[i][u - 1].affect_valeur(self.grille.grille[i][u].valeur * 2)
                        self.grille.grille[i][u].retirer_valeur()
        if ancien_liste == self.liste_act:
            break
        ancien_liste = self.liste_act


def gauche(self):
    ancien_liste = []
    while True:
        self.liste_act = []
        for i in range(len(self.grille.grille)) :
            for u in range(len(self.grille.grille[i])) :
                if  i > 0 :
                    if  self.grille.grille[i][u].remplis and not(self.grille.grille[i - 1][u].remplis) : 
                        self.liste_act.append([i, u])
                        self.grille.grille[i - 1][u].affect_valeur(self.grille.grille[i][u].valeur)
                        self.grille.grille[i][u].retirer_valeur()
                    elif self.grille.grille[i -  1][u].valeur == self.grille.grille[i][u].valeur and self.grille.grille[i][u].valeur != 0:
                        self.grille.grille[i - 1][u].affect_valeur(self.grille.grille[i][u].valeur * 2)
                        self.grille.grille[i][u].retirer_valeur()
        if ancien_liste == self.liste_act:
            break
        ancien_liste = self.liste_act

def droite(self):
    ancien_liste = []
    while True:
        self.liste_act = []
        for i in range(len(self.grille.grille)) :
            for u in range(len(self.grille.grille[i])) :
                if  i < len(self.grille.grille) - 1 :
                    if  self.grille.grille[i][u].remplis and not(self.grille.grille[i + 1][u].remplis) : 
                        self.liste_act.append([i, u])
                        self.grille.grille[i + 1][u].affect_valeur(self.grille.grille[i][u].valeur)
                        self.grille.grille[i][u].retirer_valeur()
                    elif self.grille.grille[i + 1][u].valeur == self.grille.grille[i][u].valeur and self.grille.grille[i][u].valeur != 0:
                        self.grille.grille[i + 1][u].affect_valeur(self.grille.grille[i][u].valeur * 2)
                        self.grille.grille[i][u].retirer_valeur()
        if ancien_liste == self.liste_act:
            break
        ancien_liste = self.liste_act
  