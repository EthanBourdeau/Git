import json
import os
import tkinter as tk

class Interface (tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)

        # Recupere les donnees des livres sur le fichier json associé, les convertis de dictionnaire en liste puis en instance de classe Livre
        # Maintenant que je le relis je me rends compte que ce n'est pas terrible mais le format dictionnaire est plus lisible dnas les fichiers json

        self.liste_livres = recuperation_donnees_json('donnees_livres')
        self.liste_livres = [[i['titre'], i['auteur'], i['edition'], i['emprunt']]for i in self.liste_livres]
        self.liste_livres = [Livre(i) for i in self.liste_livres]

        # Regroupe tous les livres dans une bibliotheque (classe Bibliotheque)

        self.instance_biblio = Bibliotheque(self.liste_livres)

        # Recupere les donnees des utilisateurs sur le fichier json associé, les convertis de dictionnaire en liste puis en instance de classe Utilisateur

        self.liste_utilisateurs = recuperation_donnees_json('donnees_utilisateurs')
        self.liste_utilisateurs = [[i['nom'], i['livres_empruntés']]for i in self.liste_utilisateurs]
        self.liste_utilisateurs = [Utilisateur(i[0], i[1]) for i in self.liste_utilisateurs]

        def on_close():
            """
            change le comportement de la fenetre quand on la ferme, ici quand on ferme la fenetre, les fichiers sont mis a jour avant
            """
            print(self.liste_utilisateurs)
            liste_livres_a_sauvegarder = self.instance_biblio.inventaire_livres
            donnees_livres = [Livre.to_dict(i) for i in liste_livres_a_sauvegarder]
            sauvegarde_donnees_json('donnees_livres', donnees_livres)
            donnees_users = [Utilisateur.to_dict(i)for i in self.liste_utilisateurs]
            sauvegarde_donnees_json('donnees_utilisateurs', donnees_users)
            self.quit()

        self.protocol("WM_DELETE_WINDOW", on_close)

        # taille de la fenetre
        largeur = 800 
        hauteur = 500

        # S'assure que la fenetre aparait au centre de l'ecran
        screen_largeur = self.winfo_screenwidth()
        screen_hauteur = self.winfo_screenheight()
        x = (screen_largeur // 2) - (largeur // 2)
        y = (screen_hauteur // 2) - (hauteur // 2)
        self.geometry(f"{largeur}x{hauteur}+{x}+{y}") # Definit la taille de la fenetre et empeche sa modification
        self.resizable(False, False)

        self.creer_widgets()


    def ferm_nouv_util(self):
        """
        change le comportement de la fenetre quand on la ferme, ici quand on ferme la fenetre, les fichiers sont mis a jour avant
        """
        if self.nom_nouv_util.get() != "":
            self.liste_utilisateurs.append(Utilisateur(self.nom_nouv_util.get(), []))
            self.actu_menu_deroulant()
            self.nouvelle_fenetre.destroy()


    def fenetre_util (self):
        """
        Cette fenetre s'ouvre pour creer un nouvel utilisateur
        """
        # Creation d'une fenetre secondaire
        self.nouvelle_fenetre = tk.Toplevel(self)
        self.nouvelle_fenetre.title("Nouvelle fenêtre")

        # Petit label pour informer de ce qu'il faut faire
        tk.Label(self.nouvelle_fenetre, text="Rentrez le nom du nouvel \nutilisateur et fermez cette fanetre").pack(padx=20, pady=20)

        self.nom_nouv_util = tk.StringVar()
        tk.Entry(self.nouvelle_fenetre, textvariable=self.nom_nouv_util).pack(pady=20, padx=20)

        tk.Button(self.nouvelle_fenetre, text='Creer le nouvel utilisateur', command=self.ferm_nouv_util).pack(pady=20, padx = 20)
        

    def rendre_livre(self):

        # Recupere le numero du livre selectionné (tuple du type (3,) )
        selection = self.fg_liste_livres.curselection()

        if selection:
            # Recupere le numero du livre sellectiçnné (int)
            index = selection[0]
            # A partir de l'indice recupere le nom du livre a rendre
            self.livre_a_rendre = self.fg_liste_livres.get(index)
            # Parcours les livres de la bibliotheque
            for u in self.instance_biblio.inventaire_livres:
                # Quand il trouve le livre a rendre
                if self.livre_a_rendre == u.titre:
                    # Le note comme disponible
                    u.rendre_livre()
                    # Supprime le livre de la liste des livres epruntés de l'utilisateur
                    self.util_actuel.rendre_livre(self.livre_a_rendre)
            # Supprime le livre de la listbox de l'utilisateur
            self.fg_liste_livres.delete(index)
            # Actualise la listbox des livrs dispos dans la bibliotheque
            self.actu_livres_dispos()
                
    def emprunter_livre(self):
            # Recupere le numero du livre selectionné (tuple du type (3,) )
            selection = self.fd_liste_livres_dispos.curselection()
            if selection:
                # Recupere le numero du livre sellectiçnné (int)
                index = selection[0]
                # A partir de l'indice recupere le nom du livre a emprunter
                livre_a_emprunter = self.fd_liste_livres_dispos.get(index)
                # Parcours les livres de la bibliotheque
                for i in self.instance_biblio.inventaire_livres:
                    # Quand il trouve le livre a emprunter
                    if livre_a_emprunter == i.titre:
                        # Signale a la biblio que le livre est maintenant eprunté
                        i.emprunter()
                        # Ajoute le livre a la liste de slivres empruntés par l'utilisateur
                        self.util_actuel.emprunter_livre(livre_a_emprunter)
                
                # Supprime le livre de la listbox de la bibliotheque
                self.fd_liste_livres_dispos.delete(index)
                # Actualise la listbox des livrs empruntés par l'utilisateur
                self.actu_livres_empruntés()
                
    def selection_utilisateur(self, utilisateur):
        """
        quand on clique dans le menu deroulant sur le nom d'un utilisateur, 
        vide la listbox de gauche et la rempli par les livre empruntés par ce dernier
        """
        self.util_actuel = utilisateur
        self.fg_liste_livres.delete(0, tk.END)  # Vide la listbox
        for livre in utilisateur.livres_empruntés :
            self.fg_liste_livres.insert(tk.END, livre)

    def actu_menu_deroulant(self):
        """
        ajoute le nom des utilisateurs au menu deroulant
        """
        self.fg_menuDeroulant1.delete(0, 'end')

        for utilisateur in self.liste_utilisateurs:
            self.fg_menuDeroulant1.add_command(
                # nom de l'utilisateur
                label=utilisateur.nom,
                # Fonction appellée quand un clique sur son nom
                command=lambda u=utilisateur: self.selection_utilisateur(u)
                )
            
    def actu_livres_empruntés(self):
        """
        actualise la listbox de gauche
        """
        self.fg_liste_livres.delete(0, tk.END) # vide la listbox
        for livres in self.util_actuel.livres_empruntés :
            self.fg_liste_livres.insert(tk.END, livres)

    def actu_livres_dispos(self):
        """
        actualise la listbox de droite
        """
        self.fd_liste_livres_dispos.delete(0, tk.END) # Videnla listbox
        for nom in self.instance_biblio.inventaire_livres:
            if nom.emprunt == False :
                self.fd_liste_livres_dispos.insert(tk.END, nom.titre)
            
    def frame_gauche(self):
        
        # Bouton pour creer un nouvel utilisateur ( pas encore fonctionnel)
        self.fg_btn_creer_utiliateur = tk.Button(self.frame_utilisateur,text="Nouvel \nutilisateur", relief = 'raised',font = ('Arial, 10'),activebackground='#2E5360', bg = '#74D0F1', command= self.fenetre_util)
        self.fg_btn_creer_utiliateur.grid(row = 0, column = 0, padx= 20 ,pady = 10, ipadx= 10)

        # Menu deroulant 
        self.fg_menuUtilisateurs = tk.Menubutton(self.frame_utilisateur, text='Séléctionner un utilisateur', borderwidth=2, activebackground='#2E5360', relief= 'raised', bg = '#74D0F1')
        
        # Contenu du menu deroulant (ici les utilisateurs)
        self.fg_menuDeroulant1 = tk.Menu(self.fg_menuUtilisateurs)

        # Rempli les menu deroulant
        self.actu_menu_deroulant()

        self.fg_menuUtilisateurs.configure(menu = self.fg_menuDeroulant1)
        self.fg_menuUtilisateurs.grid(column=1, row = 0, padx= 20 ,pady = 10, ipadx= 20, ipady= 10)

        self.fg_label = tk.Label(self.frame_utilisateur, text = 'Livres emprunté par cet utilisateur', relief='sunken',bg = '#74D0F1')
        self.fg_label.grid(row = 1, pady= 10,padx= 10, ipadx= 70, ipady=10, columnspan=2)

        # Par default l'utilisateur selectinné est le premier de la liste
        self.util_actuel = self.liste_utilisateurs[0]

        # Crée et rempli la listbox de droite qui contient les livres emprunté par l'utilisateur selectionné
        self.fg_liste_livres = tk.Listbox(self.frame_utilisateur, selectmode=tk.SINGLE, width=55, height=19, bg = "#CDEFFB")
        self.actu_livres_empruntés()
        self.fg_liste_livres.grid(row = 2, pady=10,columnspan=2)

        # Bouton pour rendre un livre
        self.btn_rendre_livre = tk.Button(self.frame_utilisateur, text="Rendre le livre",relief= 'raised', command= self.rendre_livre , font = ('Arial', 10), bg = '#74D0F1')
        self.btn_rendre_livre.grid(row = 3, pady=5, padx = 5,ipadx=25,columnspan=2)

    def frame_droite(self):

        self.fd_label_livres_dispos = tk.Label(self.frame_bib, text = 'Livres disponibles', relief='sunken', bg = '#74D0F1')
        self.fd_label_livres_dispos.grid(row = 1, pady= 10,padx= 45, ipadx= 120, ipady = 10, columnspan=2)

        # Cree et rempli la listbox de droite contanant les livres non empruntés
        self.fd_liste_livres_dispos = tk.Listbox(self.frame_bib, selectmode=tk.SINGLE, width=60, height=22, bg = "#CDEFFB")
        self.actu_livres_dispos()
        self.fd_liste_livres_dispos.grid(row = 2, pady=10,columnspan=2)

        # Bouton pour emprunter un livre
        self.fd_btn_emprunter = tk.Button(self.frame_bib, text="Emprunter le livre", command= self.emprunter_livre , font = ('Arial', 10),bg = '#74D0F1', relief='raised')
        self.fd_btn_emprunter.grid(row = 3, pady=5, padx = 5,ipadx=25,columnspan=2)

    def creer_widgets(self):

        # Frame principale
        self.frame = tk.Frame(self, bg = '#74D0F1' )
        
        # Frame de gauche (globalement ce qui concerne les utilisateurs)
        self.frame_utilisateur = tk.Frame(self.frame, bg = '#74D0F1')

        # Frame de droite (globalement ce qui concerne le stock de la bibliotheque)
        self.frame_bib = tk.Frame(self.frame ,bg = '#74D0F1')

        # Remplis les frame de ci - dessus
        self.frame_gauche()
        self.frame_droite()

        # Place les frames
        self.frame_utilisateur.grid(column=0, row = 0)
        self.frame_bib.grid(column=1, row = 0, padx=10)
        self.frame.pack(fill = 'both', expand = True)

class Livre :
    def __init__(self, donnees_livre):
        """ 
        args :
            donnees_livre (list) : liste des infos du livres dont son titre, auteur, edition, statut de disponibilité
        """
        self.titre = donnees_livre[0]
        self.auteur = donnees_livre[1]
        self.edition = donnees_livre[2]
        self.emprunt = donnees_livre[3]

    def to_dict(self):
        """ Mets tous les atributs de l'instance dans un dictionnaire """
        return {
            "titre" : self.titre,
            "auteur": self.auteur,
            "edition": self.edition,
            "emprunt": self.emprunt
            }

    def from_dict(Livre, data):
        """ A partir d'un dictionnaire, retourne une instance de classe dont les atributs sont les values diu dictionnaire"""
        print(data)
        return Livre([data["titre"], data["auteur"], data["edition"], data['emprunt']])
    
    def rendre_livre (self):
        self.emprunt = False
    
    def emprunter(self):
        self.emprunt = True

class Bibliotheque :

    def __init__(self, inventaire):
        self.inventaire_livres = inventaire

class Utilisateur :
    def __init__(self, n, l):
        """
        args :
            n (str) : nom de l'utilisateur
            l(list) : liste des livres empruntés par l'utilisateur
        """
        self.nom = n
        self.livres_empruntés = l

    def to_dict(self):
        """ Mets tous les atributs de l'instance dans un dictionnaire """
        return {
            "nom" : self.nom,
            "livres_empruntés": self.livres_empruntés,

            }

    def from_dict(Livre, data):
        """ A partir d'un dictionnaire, retourne une instance de classe dont les atributs sont les values diu dictionnaire"""
        print(data)
        return Livre([data["nom"], data["livres_empruntés"]])
    
    def rendre_livre (self, livre_a_rendre):
        self.livres_empruntés.remove(livre_a_rendre)
    
    def emprunter_livre (self,  livre_emprunter):
        self.livres_empruntés.append(livre_emprunter)
        
def setup_chemins():
    """
    Recupere le chemin absolu du fichier et change l'environnement d'execution pour etre dans le dossier du fichier 
    (necessaire car avec vs code le code ne s'execute pas dans le fichier ou sont situés les fichiers json dont j'ai bersoin)
    """
    chemin_absolu = os.path.abspath(__file__)
    dossier_du_fichier = os.path.dirname(chemin_absolu)
    os.chdir(dossier_du_fichier)

def sauvegarde_donnees_json(nom_fichier, donnees_a_charger):
    """
    args :
        nomm_fichier (str)
        donnee_a_charger (list)
    """
    setup_chemins()
    with open(f'{nom_fichier}.json', 'w', encoding='utf-8') as f:
        json.dump(donnees_a_charger, f, ensure_ascii=False, indent=4)

def recuperation_donnees_json(nom_fichier):
    """
    args:
        nom_fichier (str)
    """
    setup_chemins()
    with open(f'{nom_fichier}.json', 'r', encoding='utf-8') as f:
        donnees_chargees = json.load(f)
    return donnees_chargees

# Code principal
setup_chemins()
it = Interface()
it.mainloop()


