import random as rd

def grille_vide():
    return [[0 for i in range(7)] for u in range (6)]

def affiche(g):
    symbole = ["*", "X", "O"]
    for i in g:
        for u in i:
            print(symbole[int(u)], end = " ")
        print()

def coup_possible(g, c):
    for i in range(len(g)):
        if g[i][c] == 0:
            return True
    return False

def jouer(g, j, c):
    if coup_possible(g, c):
        i = 0
        while i + 1 < len(g) and g[i + 1][c] == 0:
            i += 1
        g[i][c] = j
    else :
        print("Colone pleine, coup impossible")

def horizontal(g, j, l, c):
    if c + 3 > len(g[l]) - 1:
        return False
    else:
        for i in range(4):
            if g[l][c + i] != j:
                return False
        return True
    

def vertical(g, j, l, c):
    if l + 3 > len(g) - 1:
        return False
    else:
        for i in range(4):
            if g[l + i][c ] != j:
                return False
        return True

def diag_bas(g, j, l, c):
    if l + 3 > len(g) - 1 or c + 3 > len(g[l]) - 1:
        return False
    else:
        for i in range(4):
            if g[l + i][c + i] != j:
                return False
        return True

def diag_haut(g, j, l, c):
    if l- 3 < 0 or c + 3 > len(g[l]) - 1:
        return False
    else:
        for i in range(4):
            if g[l - i][c + i] != j:
                return False
        return True
    
def victoire(g, j):
    fcts = [horizontal, vertical, diag_bas, diag_haut]
    for i in range(len(g)):
        for u in range(len(g[i])):
            for fct in fcts:
                if fct(g, j, i, u):
                    print(f'Le joueur numero {j} a gagné')
                    return True
    return False
    
def match_nul(g):
    for i in g[0]:
        if i == 0:
            return False
    return True

def coup_aleatoire(g, j):
    if not(match_nul(g)):
        ligne_aleat = rd.randint(0, 6)
        while not(coup_possible(g, ligne_aleat)):
            ligne_aleat = rd.randint(0, 6)
        jouer(g, j, ligne_aleat)
    else :
        print('Partie finie, match nul')

def partie_aleatoire():
    g = grille_vide()
    affiche(g)
    partie_en_cours = True
    while partie_en_cours:
        for i in [1, 2]:
            coup_aleatoire(g, i)
            if victoire(g, i):
                affiche(g)
                partie_en_cours = False
                break

def partie():
    g = grille_vide()
    partie_en_cours = True
    while partie_en_cours:
        affiche(g)
        x = int(input('Numero de la ligne')) - 1
        jouer(g, 1, x)
        if victoire(g, 1):
            affiche(g)
            partie_en_cours = False
            break
        coup_aleatoire(g, 2)
        if victoire(g, 2):
            affiche(g)
            partie_en_cours = False
            break








    

