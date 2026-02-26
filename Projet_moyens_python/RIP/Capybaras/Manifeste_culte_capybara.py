import tkinter as tk
import os
from PIL import Image, ImageTk


class Interface (tk.Tk):
    def __init__(self):
        super().__init__()
        setup_chemins()
        self.creer_fen(self, 1080, 720)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mode = 'bv'
        self.app_wid()

    def app_wid (self):
        
        self.bt_frame = tk.Frame(self)
        self.frame_flex = tk.Frame(self, background = '#AE21FF')
        pages = [self.frame_convic, self.frame_infos]
        list = ['A propos de nous', 'Nos convictions', 'Nous contcter']
        for i in range (len(list)):
            tk.Button(self.bt_frame, text=list[i], command=pages[i-1] ,  
                      height=2, width = 32, 
                      relief='flat', bg = '#C35CFF', 
                      fg = 'white',font=("Century Gothic", 14)).grid(column=i+1, row = 0)
        self.frame_bienvenue()

        self.bt_frame.grid(column=0, row= 0, sticky = 'nsew')
        self.frame_flex.grid(column=0, row = 1, sticky= 'nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def frame_bienvenue (self):
        tk.Label(self.frame_flex, text="Bienvenue dans l'eglise du saint capybara", 
                 font=("Century Gothic", 28), 
                 bg = '#AE21FF', fg = 'white').pack(pady=20)
        
    def frame_convic(self):
        self.vider_frame()
        txt_convic = recuperation_donnees("Texts/Convic")
        tk.Label(self.frame_flex, text=txt_convic, wraplength=1000, font=("Century Gothic", 20), bg = '#AE21FF', fg = 'white').pack(expand= True)
        
    
    def frame_infos (self):
        self.vider_frame()
        image_originale = Image.open("Imgs/Diagramme_orga.png")
        image_redim = image_originale.resize((1000, 350), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image_redim)
        canvas = tk.Canvas(self.frame_flex, width=400, height=300, highlightthickness=0, bg = '#AE21FF')
        canvas.pack(padx = 20, fill='both', expand=True)
        canvas.create_image(0, 0, image=self.bg_image, anchor='nw')

    def frame_contact(self):
        self.vider_frame()

    def on_close(self):
        self.nouvelle_fenetre = tk.Toplevel(self)
        self.creer_fen(self.nouvelle_fenetre, 400, 300)

        image_originale = Image.open("Imgs/Capy_tronc.png")
        image_redim = image_originale.resize((400, 300), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image_redim)

        canvas = tk.Canvas(self.nouvelle_fenetre, width=400, height=300, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=self.bg_image, anchor='nw')
        canvas.create_text(200, 250, text=recuperation_donnees("Texts/Slogan"), fill='yellow',
                        font=("Century Gothic", 14), anchor='center')
        self.after(1000, self.quit)


    def creer_fen (self, fen, l, h):
        screen_largeur = self.winfo_screenwidth()
        screen_hauteur = self.winfo_screenheight()
        x = (screen_largeur // 2) - (l // 2)
        y = (screen_hauteur // 2) - (h // 2)
        fen.geometry(f"{l}x{h}+{x}+{y}") # Definit la taille de la fenetre et empeche sa modification
        fen.resizable(False, False)     
    
    def vider_frame(self):
        for widget in self.frame_flex.winfo_children():
            widget.destroy()


def setup_chemins():
    chemin_absolu = os.path.abspath(__file__)
    dossier_du_fichier = os.path.dirname(chemin_absolu)
    os.chdir(dossier_du_fichier)

def recuperation_donnees(nom_fichier):
    setup_chemins()
    chemin_complet = os.path.join(os.getcwd(), f"{nom_fichier}.txt")
    
    if not os.path.exists(chemin_complet):
        raise FileNotFoundError(f"Fichier introuvable : {chemin_complet}")
    
    with open(chemin_complet, 'r', encoding='utf-8') as f:
        return f.read()
    
it = Interface()
it.mainloop()