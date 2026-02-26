import tkinter as tk

valeurs_utilisateur = {}

class Interface_valeurs(tk.Tk):

    def __init__(self):
        self.valeurs_utilisateur = {}
        tk.Tk.__init__(self)

        def on_close():
            self.quit()

        self.protocol("WM_DELETE_WINDOW", on_close)
        largeur = 300 # taille de la fenetre
        hauteur = 175

        screen_largeur = self.winfo_screenwidth()
        screen_hauteur = self.winfo_screenheight()

        x = (screen_largeur // 2) - (largeur // 2)
        y = (screen_hauteur // 2) - (hauteur // 2)

        self.geometry(f"{largeur}x{hauteur}+{x}+{y}") # Definit la taille de la fenetre et empeche sa modification
        self.resizable(False, False)
        self.creer_widgets()

    def creer_widgets(self):

        def f_valider(self): # Fonction activée a l'appui du bouton 
            print(self.nbr_j)
            joueurs = self.nbr_j.get() # Récupere les valeurs de l'utilisateur
            parties = self.nbr_p.get()

            if joueurs == "" and parties == "": # Verifie que l'utilisateur a bien rentré quelque chose
                self.text_label.set("Entrez des valeurs")
            elif joueurs == "":
                self.text_label.set("Entrez un nombre de joueurs")
            elif parties == "":
                self.text_label.set("Entrez un nombre de parties")
            elif int(joueurs) % 10 != 0:
                self.text_label.set("Le nombre de joueurs doit etre divisible par 10")
            else:
                try: # convertis les valeurs en int
                    self.valeurs_utilisateur["joueurs"], self.valeurs_utilisateur["parties"] = int(joueurs), int(parties) 
                    # Si l'utilisateur a rentré des valeurs correctes, les valeurs de retour sont mises a jours
                    self.destroy()  # Ferme la fenêtre pour continuer l'exécution du reste du programme
                except ValueError:
                    self.text_label.set("Mauvais type de valeurs") # Sinon, un message est affiché

        self.frame = tk.Frame(self)
        self.frame.pack()

        self.text_label = tk.StringVar()
        self.label_1 = tk.Label(self.frame, textvariable=self.text_label).pack(pady=5)
        self.text_label.set("Entrez un nombre de joueurs et de parties")

        self.entry_frame = tk.Frame(self.frame)
        self.entry_frame.pack()

        self.label_2 = tk.Label(self.entry_frame, text="Nombre de joueurs").grid(row=0, column=0) # Crée une zone de texte avec une etiquette a coté
        self.nbr_j = tk.Entry(self.entry_frame)
        self.nbr_j.grid(row=0, column=1, padx=10, pady=5)

        self.label_3 = tk.Label(self.entry_frame, text="Nombre de parties").grid(row=1, column=0) # Meme chose pour le nombre de parties
        self.nbr_p = tk.Entry(self.entry_frame)
        self.nbr_p.grid(row=1, column=1, padx=10, pady=5)

        self.bouton = tk.Button(self.frame, text="Valider", command=lambda : f_valider(self)).pack(pady=10)

interface = Interface_valeurs() 

interface.mainloop()

print(interface.valeurs_utilisateur)