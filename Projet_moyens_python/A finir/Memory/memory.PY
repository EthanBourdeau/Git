import random
import tkinter as tk
from PIL import Image, ImageTk
import os
import json
# from Game_class import Game

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        H,W = 800,  800
        self.hauteur = 20
        self.largeur = 10
        self.creer_fen( H, W)
        self.config(bg="#FFFFFF")
        self.entete = tk.Frame(self,bg="#A0A02E", width=W, height=H*0.2)
        self.frame = tk.Frame(self, bg="#A0A02E", width=W, height=H*0.8)
        self.creation_entete()
        self.creation_zone_jeu()
        self.init_variables()
        self.entete.pack()
        self.entete.pack_propagate(False)
        #self.jeu = Game()
        self.frame.pack()

    def creation_entete(self):
        tk.Label(self.entete, text = 'Jeu du memory', bg="#A0A02E", font=('Arial', 30)).pack(pady=20)

    def init_variables(self):
        pass

    #def creation_zone_jeu(self):
        ##cote=150
        #img = Image.open(r"C:\Users\tatan\Desktop\Perso\Git\Projet_moyens_python\A finir\Memory\Illustrations\Capybara.png")
        #img = img.resize((cote, cote))
        #self.photo = ImageTk.PhotoImage(img)
        #for i in range(4):
        #    for y in range(5):
        #        self.a = tk.Button(self.frame, image=self.photo, width= cote, height = cote)
        #        self.a.grid(row = i, column = y)
  
    def creation_zone_jeu(self):
        cote=10
        nombres = list(range(10))+list(range(10)) 
        self.boutons = [] 
        self.liste_nombres = []
        random.shuffle(nombres)
        for i in range(4):
            list_temp = []
            for y in range(5):            
                self.a = tk.Button(self.frame , width= cote*2, height = cote, bg = 'lightgray')
                nbr = nombres.pop()
                bout = MonBouton(nbr, self.a)
                bout.tk_button.config(command = lambda co_i = i, co_y = y  :self.reveler_bouton((co_i, co_y)))
                bout.tk_button.grid(row = i, column = y)
                list_temp.append(bout)
            self.boutons.append(list_temp)

    def reveler_bouton(self, c):
        self.compter_boutons()
        
        if len(self.boutons_reveles) == 2:
            if self.boutons_reveles[0].nombre_corr == self.boutons_reveles[1].nombre_corr:
                self.boutons_reveles[0].paire, self.boutons_reveles[1].paire = True, True
                
            else:
                self.boutons_reveles[0].revele, self.boutons_reveles[1].revele = False, False
        self.compter_boutons()
        self.maj_boutons()
        i, y = c
        bouton = self.boutons[i][y]
        bouton.tk_button.config(text = str(bouton.nombre_corr) , bg = 'white')
        if not bouton.revele:
            self.boutons_reveles.append(bouton)
            bouton.revele = True
    
    def maj_boutons(self):
        for i in self.boutons:
            for y in i:
                if y.revele:
                    y.tk_button.config(text = str(y.nombre_corr), bg = 'white')
                else:
                    y.tk_button.config(text = "", bg = 'lightgray')

    def compter_boutons(self):
        self.boutons_reveles = []
        for i in self.boutons:
            for y in i:
                if y.revele and not y.paire:
                    self.boutons_reveles.append(y)

    def creer_fen(self, l, h):
        screen_largeur = self.winfo_screenwidth()
        screen_hauteur = self.winfo_screenheight()
        x = (screen_largeur // 2) - (l // 2)
        y = (screen_hauteur // 2) - (h // 2)
        self.geometry(f"{l}x{h}+{x}+{y}")
        self.resizable(False, False)

class MonBouton:
    def __init__(self, n, b):
        self.paire = False
        self.revele = False
        self.nombre_corr = n
        self.tk_button = b



    



it = Interface()
it.mainloop()