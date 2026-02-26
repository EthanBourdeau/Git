import random
import time
from copy import deepcopy

def premiere_grille(taille):
    grille = [[random.choice(["□", "■"]) for i in range(taille)] for u in range(taille)]
    return grille

def affichage(grille):
    taille_de_ligne = 0
    for sous_liste in grille:
        for carré in sous_liste:
            print(carré, end= " ")
            taille_de_ligne = taille_de_ligne + 1
            if taille_de_ligne  == len(grille):
                taille_de_ligne = 0
                print()

def compter_voisins(grille, cordX, coordY):
    voisins = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i==0 and j==0):
                if 0 <= cordX+i < len(grille) and 0 <= coordY+j < len(grille):
                    if grille[cordX+i][coordY+j] == "■":
                        voisins = voisins + 1
    print(voisins)
    return voisins

def gen_suivante (grille):
    new_grille = deepcopy(grille)
    for cordX in range(len(grille)):
        for coordY in range(len(grille)):
            voisins = compter_voisins(grille, cordX, coordY)
            if grille[cordX][coordY] == "■" and (voisins < 2 or voisins > 3):
                new_grille[cordX][coordY] = "□"
            elif grille[cordX][coordY] == "□" and voisins == 3:
                new_grille[cordX][coordY] = "■"
    return new_grille

def jeu_vie(taille, iterations):
    grille = premiere_grille(taille)
    affichage(grille)
    for i in range(iterations):
        grille = gen_suivante(grille)
        time.sleep(0.5)
        print(" ")
        affichage(grille)

jeu_vie(10, 10)