import random as rd
import tkinter as tk

import json
import os

"""
Ceci est le jeu du demineur, il génére une grille de maniere aleatoire.
Un clic passe la case en rouge (utilisé pour marquer une bombe), un deuxieme appui la revele et indiquant son nombre de bombes voisines 
Une case bleue est donnée au debut pour aider sur le premier clic
Il y a 1 bombes toutes les 4 case, soit 156 pour une grille de 25*25
"""

class Interface (tk.Tk):
    """
    Génére la grille et les methodes associées
    """
    def __init__(self):
        self.jeu_en_cours = True
        self.nbr_carrés = self.demander_taille()

        tk.Tk.__init__(self)
        self.title('Jeu du demineur')
        self.liste_tuiles = Grille(self.nbr_carrés)
        # taille de la fenetre
        self.largeur = 830
        self.hauteur = 890
        # S'assure que la fenetre aparait au centre de l'ecran
        screen_largeur = self.winfo_screenwidth()
        screen_hauteur = self.winfo_screenheight()
        x = (screen_largeur // 2) - (self.largeur // 2)
        y = (screen_hauteur // 2) - (self.hauteur // 2)
        self.geometry(f"{self.largeur}x{self.hauteur}+{x}+{y}") # Definit la taille de la fenetre et empeche sa modification
        self.resizable(False, False)
        #self.iconbitmap('Demineur_icone.ico')
        self.config(bg = 'green')
        self.creer_widgets()
        

    def defaite (self):
        self.jeu_en_cours = False
        #self.sauv_new_best()
        self.fenetre_fin('Vous avez perdu')
        
    def sauv_new_best(self):
        recs = self.recuperation_donnees_json('Reccords_demineur.json')
        for i in recs.keys():
            if int(i) == self.nbr_carrés  :
                if int(recs[i]) > self.temps_actu.get():
                    self.sauvegarde_donnees_json('Reccords_demineur.json', {self.nbr_carrés : self.temps_actu.get()})
            else:
                self.sauvegarde_donnees_json('Reccords_demineur.json', {self.nbr_carrés : self.temps_actu.get()})

    def victoire (self):
        self.jeu_en_cours = False
        self.sauv_new_best()
        self.fenetre_fin('Vous avez gagné')


    def demander_taille(self):
        def aff():
            nonlocal result
            try:
                result = int(val.get())
                if result > 35 or result < 5 :
                    raise ValueError
            except ValueError:
                result = None
            fen.destroy()

        fen = tk.Tk()
        fen.title("Choix de la taille")
        tk.Label(fen, text='Entrez une valeur entre 5 et 35').pack(pady = 10)
        val = tk.StringVar()
        tk.Entry(fen, textvariable=val).pack()
        tk.Button(fen, text='Valider', command=aff).pack(pady = 10)

        result = None
        fen.wait_window()  # Attend que la fenêtre soit fermée
        return result
    
    def recup_tps_int(self):
        heure_str = self.temps_actu.get().split(':')
        heure_int = [int(i) for i in heure_str]
        
        return heure_int

    def commence_chrono(self):
        heure_int = self.recup_tps_int()

        # Augmentation de 1 seconde et mise a jour de la minute suivante
        heure_int[1] += 1
        if heure_int[1] == 60 :
            heure_int[1] = 00
            heure_int[0] += 1

        # Assure que le temps est au format 00:00 
        for i in range(len(heure_int)):
            heure_int [i] = str(heure_int[i])
            if len(heure_int[i]) == 1:
                heure_int[i] ='0'+  heure_int[i]
        
        heure_retour = f'{heure_int[0]}:{heure_int[1]}'
        self.temps_actu.set(heure_retour)
        if self.jeu_en_cours :
            self.after(1000, self.commence_chrono)

    def creation_chrono(self):
        self.temps_actu = tk.StringVar()
        self.temps_actu.set('00:00')
        tk.Label (self, textvariable = self.temps_actu, bg = "#aad751", width=7, height=1).pack(pady = 5)

    def creer_widgets (self):
        self.creation_chrono()
        self.main_frame = tk.Frame(self, height = 800, width = 800)
        self.ajouter_carrés()
        self.indice()
        self.main_frame.pack(padx = 10, pady = 10)
        self.commence_chrono()

    def indice(self):
        """
        Ajoute un carré bleu qui indique une case sans danger (Sans cela le debut serait frustrant)
        """
        a = [i for u in self.liste_tuiles.grille for i in u if (not(i.miné) and i.voisins == 0)]
        tuile_verte = rd.choice(a)
        tuile_verte.bt.config(bg = '#4E6997')

    def ajouter_carrés(self) :
        """ Rempli la fenetre de boutons """
        t_case = 800 // self.nbr_carrés
        for ligne in range(len(self.liste_tuiles.grille)):
            for colone in range(len(self.liste_tuiles.grille[ligne])) :
                if ligne % 2 == 0:
                    if colone % 2 == 1 :
                        self.liste_tuiles.grille[ligne][colone].bg_clair = False
                else :
                    if colone % 2 == 0:
                        self.liste_tuiles.grille[ligne][colone].bg_clair = False

                if self.liste_tuiles.grille[ligne][colone].bg_clair :
                    coul = '#aad751'
                else :
                    coul = '#a2d149'

                bouton = tk.Button(self.main_frame, text="", bg=coul, bd = 0)
                bouton.config(command = lambda u = self.liste_tuiles.grille[ligne][colone], b = bouton :self.on_clic(u, b))
                self.liste_tuiles.grille[ligne][colone].bt = bouton
                bouton.place(y = ligne* t_case, x = colone*t_case,width=t_case, height=t_case)

    def on_clic(self, la_tuile, bouton):
        """
        Vérifie le bouton cliqué, si il est caché et rouge, il le revele, puis verifie si ce n'etais pas une bombe
        Si le bouton etait caché et gris, il le pass en rouge
        Puis il revele toutes les voisines des tuiles avec 0 bombes voisienes
        et repete l'operation tant qu'il en trouve des nouvelles
        """
        if self.jeu_en_cours :
            if la_tuile.caché:
                if la_tuile.danger:
                    if la_tuile.miné:
                        self.defaite()
                    else :
                        self.reveler_tuile(la_tuile)
                else :
                    la_tuile.danger = True
                    bouton.config(bg = 'red')
            else:
                """
                Révele automatiquement les tuiles restantes si on a deja identifié toutes le bombes autour d'une case
                """
                self.parc_voisines_rouges(la_tuile.cx, la_tuile.cy)
                if self.marquées == la_tuile.voisins:
                    self.reveler_nom_mar()
            self.ancien_liste = []
            self.rev_recurcif()
            
    def rev_recurcif(self):
        self.local_vides()
        if self.ancien_liste == self.tuiles_vides:
            return
        else:
            self.rev_t_vides()
            self.ancien_liste = self.tuiles_vides
            self.verif_vic()
            self.rev_recurcif()
        
    def reveler_nom_mar(self):
        for i in self.non_marquée :
            if not(i.miné):
                self.reveler_tuile(i)
            else :
                self.defaite()

    def parc_voisines_rouges(self, coordX, coordY):
        """ Récupere toutes les tuiles CACHEES ET NON NOTEES EN ROUGE"""
        self.marquées = 0
        self.non_marquée = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    new_x = coordX + i
                    new_y = coordY + j
                    if 0 <= new_x < len(self.liste_tuiles.grille[0]) and 0 <= new_y < len(self.liste_tuiles.grille):
                        if self.liste_tuiles.grille[new_y][new_x].danger :
                            self.marquées += 1
                        else :
                            self.non_marquée.append(self.liste_tuiles.grille[new_y][new_x])

    def fenetre_fin(self, t):
        """
        A la fin du jeu, une deuxieme fenetre s'ouvre, affiche du texte et 5 sec plus tard tout se ferme
        """
        self.nouvelle_fenetre = tk.Toplevel(self)
        l = 200
        h = 100
        # S'assure que la fenetre aparait au centre de l'ecran
        screen_largeur = self.winfo_screenwidth()
        screen_hauteur = self.winfo_screenheight()
        x = (screen_largeur // 2) - (l // 2)
        y = (screen_hauteur // 2) - (h // 2)
        self.nouvelle_fenetre.geometry(f"{l}x{h}+{x}+{y}") # Definit la taille de la fenetre et empeche sa modification
        self.nouvelle_fenetre.resizable(False, False)
        tk.Label(self.nouvelle_fenetre, text = t).pack(padx=20, pady=20)

    def reveler_tuile (self, tuile_ac):
        """ Change la couleur de la tuile en blanc et affiche son nombre de bombes voisines """
        tuile_ac.caché = False
        if tuile_ac.bg_clair:
            col = '#DCCBAD'
        else:
            col = '#C8AD7F'
        if tuile_ac.voisins > 0 :
            tuile_ac.bt.config(text = str(tuile_ac.voisins), bg = col)
        else :
            tuile_ac.bt.config(text = " ", bg = col)
        tuile_ac.danger = False

    def local_vides(self):
        """ Recupere toutes les tuiles revelées et n'ayant aucune bombes voisines """
        self.tuiles_vides = []
        for i in self.liste_tuiles.grille :
            for u in i :
                if not(u.caché) and u.voisins == 0:
                    self.tuiles_vides.append(u)

    def rev_t_vides(self):
        """ Pour chaque tuile recupérée dans la fonction précédante, on affiche tous ses voisins """
        for i in self.tuiles_vides :
            self.parc_voisins(i.cx, i.cy)
            for u in self.voisins :
                self.reveler_tuile(u)

    def parc_voisins(self, coordX, coordY):
        """ Récupere toutes les tuiles CACHEES ET NON NOTEES EN ROUGE """
        self.voisins = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    new_x = coordX + i
                    new_y = coordY + j
                    if 0 <= new_x < len(self.liste_tuiles.grille[0]) and 0 <= new_y < len(self.liste_tuiles.grille):
                        if self.liste_tuiles.grille[new_y][new_x].caché and not(self.liste_tuiles.grille[new_y][new_x].danger):
                            self.voisins.append(self.liste_tuiles.grille[new_y][new_x])

    def verif_vic (self):
        """ Vérifie si toutes les tuiles non minées sont decouvertes, si oui le jeu est fini """
        tuiles_restantes = sum(1 for ligne in self.liste_tuiles.grille for tuile in ligne if tuile.caché and not tuile.miné)
        if tuiles_restantes == 0:
            self.victoire()

    def setup_chemins(self):
        """
        Recupere le chemin absolu du fichier et change l'environnement d'execution pour etre dans le dossier du fichier 
        (necessaire car avec vs code le code ne s'execute pas dans le fichier ou sont situés les fichiers json dont j'ai bersoin)
        """
        chemin_absolu = os.path.abspath(__file__)
        dossier_du_fichier = os.path.dirname(chemin_absolu)
        os.chdir(dossier_du_fichier)

    def sauvegarde_donnees_json(self,nom_fichier, donnees_a_charger):
        """
        args :
            nomm_fichier (str)
            donnee_a_charger (list)
        """
        self.setup_chemins()
        with open(f'{nom_fichier}.json', 'w', encoding='utf-8') as f:
            json.dump(donnees_a_charger, f, ensure_ascii=False, indent=4)

    def recuperation_donnees_json(self, nom_fichier):
        """
        args:
            nom_fichier (str)
        """
        self.setup_chemins()
        with open(f'{nom_fichier}.json', 'r', encoding='utf-8') as f:
            donnees_chargees = json.load(f)
        return donnees_chargees
    
class Tuile :
    """
    Classe de toutes les tuiles
    """
    def __init__(self, x, y):
        self.miné = False
        self.caché = True
        self.danger = False
        self.cx = x
        self.cy = y
        self.bt = 0
        self.voisins = 0
        self.bg_clair = True

class Grille:
    """
    Lorsqu'lle est appelé elle génére une grille de taille n * n,
    ajoute les bombes et pour toutes les cases, calcul son nombres de bombes voisines
    """
    def __init__(self, n):
        self.grille = []
        self.valeur = n

        self.générer_grille()
        self.remplir_bombes()
        self.setup_val_voins()


    def générer_grille (self):
        """ Nom suffisament explicite"""
        self.grille  = [[Tuile(i, u) for i in range(self.valeur)]for u in range(self.valeur)]

    def remplir_bombes (self):

        i = 0
        while i < self.valeur**2 /4 : # Pourquoi 4 * n ? parceque ca me semblait etre une bonne quantité ...
            ligne = rd.choice(self.grille)
            a_miner = rd.choice(ligne)
            if not(a_miner.miné):
                a_miner.miné = True
                i += 1

    def setup_val_voins(self):
        for i in range(len(self.grille)):
            for u in range (len(self.grille[i])):
                self.grille[i][u].voisins = self.compter_voisins(i, u)

    def compter_voisins(self, coordX, coordY):
        """ Fonction quasiment identique a celle utilisée dans le prjet jeu de la vie """
        voisins = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i==0 and j==0):
                    if 0 <= coordX+i < len(self.grille) and 0 <= coordY+j < len(self.grille):
                        if self.grille[coordX+i][coordY+j].miné :
                            voisins = voisins + 1
        return voisins

i = Interface()
i.mainloop()
