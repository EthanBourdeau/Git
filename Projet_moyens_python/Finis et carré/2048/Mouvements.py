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

def mouv_bas(self):
     g1()
     g2()

def g1(self):
        self.liste_act = []
        for i in range(len(self.grille.grille)) :
            for u in range(len(self.grille.grille[i])) :
                if  u < len(self.grille.grille) - 1 and self.grille.grille[i][u].remplis and not(self.grille.grille[i][u + 1].remplis)  :
                    self.liste_act.append([i, u])

def g2(self):
    for i in self.liste_act :
        self.grille.grille[i[0]][i[1] + 1].affect_valeur(self.grille.grille[i[0]][i[1]].valeur)
        self.labels[i[0]][i[1] + 1].config(bg = COLS[f'col_{self.grille.grille[i[0]][i[1] + 1].valeur}'], text = self.grille.grille[i[0]][i[1] + 1].valeur)
        self.grille.grille[i[0]][i[1]].retirer_valeur()
        self.labels[i[0]][i[1]].config(bg = COLS['col_0'], text = ' ')