import random
import matplotlib.pyplot as plt
import tkinter as tk

valeurs_utilisateur = {}

def Interface_valeurs():

    def f_valider(): # Fonction activée a l'appui du bouton 
        
        joueurs = nbr_j.get() # Récupere les valeurs de l'utilisateur
        parties = nbr_p.get()

        if joueurs == "" and parties == "": # Verifie que l'utilisateur a bien rentré quelque chose
            text_label.set("Entrez des valeurs")
        elif joueurs == "":
            text_label.set("Entrez un nombre de joueurs")
        elif parties == "":
            text_label.set("Entrez un nombre de parties")
        elif int(joueurs) % 10 != 0:
            text_label.set("Le nombre de joueurs doit etre divisible par 10")
        else:
            try: # convertis les valeurs en int
                valeurs_utilisateur["joueurs"], valeurs_utilisateur["parties"] = int(joueurs), int(parties) 
                # Si l'utilisateur a rentré des valeurs correctes, les valeurs de retour sont mises a jours
                root.destroy()  # Ferme la fenêtre pour continuer l'exécution du reste du programme
            except ValueError:
                text_label.set("Mauvais type de valeurs") # Sinon, un message est affiché

    def on_close():
        root.quit()

    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_close) # Change la consequence du fait de apppuyer sur le X de fermeture 
    #pour l'action de la fonctione en argument ici root.quit() (Chat gpt)
    
    largeur = 300 # taille de la fenetre
    hauteur = 175

    screen_largeur = root.winfo_screenwidth()
    screen_hauteur = root.winfo_screenheight()

    x = (screen_largeur // 2) - (largeur // 2)
    y = (screen_hauteur // 2) - (hauteur // 2)

    root.geometry(f"{largeur}x{hauteur}+{x}+{y}") # Definit la taille de la fenetre et empeche sa modification
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack()

    text_label = tk.StringVar()
    tk.Label(frame, textvariable=text_label).pack(pady=5)
    text_label.set("Entrez un nombre de joueurs et de parties")

    entry_frame = tk.Frame(frame)
    entry_frame.pack()

    tk.Label(entry_frame, text="Nombre de joueurs").grid(row=0, column=0) # Crée une zone de texte avec une etiquette a coté
    nbr_j = tk.Entry(entry_frame)
    nbr_j.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(entry_frame, text="Nombre de parties").grid(row=1, column=0) # Meme chose pour le nombre de parties
    nbr_p = tk.Entry(entry_frame)
    nbr_p.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(frame, text="Valider", command=f_valider).pack(pady=10)

    root.mainloop()

class Joueur ():
    def __init__(self, skill):
        """
        Definit les stats de tous les joueurs
        """
        self.skill = skill
        self.elo = random.random()
        self.liste_elo = []


    def modif_elo_joueur(self, num_modif):
        """
        le nom est assez explicite
        """
        self.elo+= num_modif
        self.liste_elo.append(self.elo)

class Liste_joueurs:

    def __init__(self, nombre_joueurs):
        """
        crée une liste d'instances de la classe Joueurs aussi longue qu'on veut de joueurs
        """
        self.liste = []
        for i in range(nombre_joueurs):
            self.liste.append(Joueur(i))
   
    def tri_elo(self):
        """
        tri la liste par elo
        """
        self.liste = sorted(self.liste, key=lambda u : u.elo)

    def repartition (self):
        """
        change la liste,  en liste de liste de 2 listes
        """
        liste_temporaire =list()
        for p in range(int(len(self.liste)/10)):
            partie = self.liste[p*10:(p+1)*10]
            random.shuffle(partie)
            liste_temporaire.append([partie[0:5],partie[5:10]])
        self.liste = liste_temporaire
    
    def deter_score (self, partie_en_cours, equipe):
        """ Compte le score total d'une equipe en additionnat le skill de tous les joueurs"""
        ret = 0
        for f in equipe:
            ret += f.skill
        return ret

    def deter_gag (self, partie_en_cours):
        """ 
            a partir du score de chaque equipes, 
            determine le gagnant et renvoie une liste informant de 
            1/ l'equipe gagnante 2/ si l'ecart de niveau etait considerable
        
        Args :
            liste_joueurs : explicite
            partie_en_cours : une fraaction de self,  celle sur laquelle on travaille actuellement

        """
        sc1 = self.deter_score(partie_en_cours, partie_en_cours[0])
        sc2 = self.deter_score(partie_en_cours, partie_en_cours[1])
        if sc1 == sc2 :
            return [random.choice([0,1]), 0]
        elif sc1 < sc2:
            if sc2 > sc1 +sc1/2:
                return [1, 1]
            else :
                return  [1,0]
        else :
            if sc1 > sc2 +sc2/2:
                return [0, 1]
            else :
                return  [0, 0]
    
    def simul_partie(self):
        """ Simule une partie en renvoyant une liste de liste contenant 
        le numero des equipes gagnantes et de l'info de si l'ecart de niveau etait important
        """
        list_g  = []
        for u in self.liste:
            list_g.append(self.deter_gag(u))
        return list_g
    
    def modif_elo_equipe(self, equipe_courante, num_modif):
        """ 
        appelle la methode modif_elo_joueurs de la classe Joueurs en lui indiquant la modificatiion a effectuer (quantité d'elo a retirer / ajouter)
        """
        for u in equipe_courante:
            u.modif_elo_joueur(num_modif)

    def evol_elo(self, liste_equipes_gagnantes):
        """ 
        Determine quels joueurs ont gané / perdu et modifie leur elo en consequence 
        
        Args :
            liste_equipes_gagnantes : liste des equipes gagnantes sous ce format : [[numero_de_equipe_gagnante 0 ou 1, grand_ecart (oui = 1, non = 0)], [numero_de_equipe_gagnante 0 ou 1, grand_ecart (oui = 1, non = 0)]]

        """
        for u in range (len(self.liste)) :
            eqp_gag = self.liste[u][liste_equipes_gagnantes[u][0]]
            eqp_perd = self.liste[u][abs(liste_equipes_gagnantes[u][0]-1)]
            eqp_perd = self.modif_elo_equipe(eqp_perd, -25)
            if liste_equipes_gagnantes[u][1] == 1:
                eqp_gag = self.modif_elo_equipe(eqp_gag, 25)
            else :
                eqp_gag = self.modif_elo_equipe(eqp_gag, 45)

    def form (self):
        """
        Transforme la liste de listes de listes en une seule liste
        """
        self.liste = [y for u in self.liste for v in u for y in v]

    def exec_tour(self):
        """
        Execute toutes les etapes d'un tour
        """
        self.tri_elo()
        self.repartition()
        liste_equipes_gagnantes = self.simul_partie()
        self.evol_elo(liste_equipes_gagnantes)
        self.form()


def affiche_resultats(innstance_classe_joueurs):
    """ Affiche le graphique """
    y = [i for i in range(len(innstance_classe_joueurs.liste[0].liste_elo))]
    for x in innstance_classe_joueurs.liste:
        plt.plot(y, x.liste_elo, color="k")
    plt.title("Evolution elos")
    plt.xlabel("Nbr parties")
    plt.ylabel("Elo")
    plt.show()

def lancement_simulation ():
    """Code principale, on y retouve la boucle principale"""
    Interface_valeurs()
    if "joueurs" not in valeurs_utilisateur or "parties" not in valeurs_utilisateur:
        print("Simulation annulée par l'utilisateur.")
        return 
    nbr_joueurs = valeurs_utilisateur['joueurs']
    nbr_parties = valeurs_utilisateur['parties']
    joueurs = Liste_joueurs(nbr_joueurs)
    for _ in range (nbr_parties):
        joueurs.exec_tour()
    affiche_resultats(joueurs)

lancement_simulation()

