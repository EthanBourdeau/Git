import tkinter as tk
import random

def gener_seq():
    couleurs = ['rouge', 'vert', 'jaune', 'bleu', 'violet', 'rose']
    return [random.choice(couleurs) for i in range(4)]

vies_joueur = 10
sequence = gener_seq()

def verif_reponse(reponse, joueur):
    comparaison = []
    for m in range(4):
        if reponse[m] == joueur[m]:
            comparaison.append('Correct')
        elif joueur[m] in reponse:
            comparaison.append('Mal placé')
        else : 
            comparaison.append('Mauvais')
    return comparaison

def afficher_texte(couleur):
    ref = ['rouge', 'vert', 'jaune', 'bleu', 'violet', 'rose']
    texte_actu = txt_label.get()
    if len(texte_actu.split()) == 4 or texte_actu.split()[0] not in ref:
        texte_actu = ''
    txt_label.set(texte_actu + ' ' + couleur)
    if len(txt_label.get().split()) == 4 :
        txt_deux_label.set(txt_label.get())
    print(txt_label.get())
    verif_taille()
    

def verif_taille():
    global vies_joueur
    global sequence
    msg_affich = txt_label.get()
    if len(msg_affich.split()) == 4:
        infos_joueur = msg_affich.split()
        if infos_joueur == sequence:
            txt_label.set('Bien joué')
            root.after(2000, root.destroy)
        else :
            nouveau_message = ' '.join(verif_reponse(sequence, infos_joueur))
            txt_label.set(nouveau_message)
        vies_joueur -= 1
        print(vies_joueur)
        if vies_joueur == 0:
            txt_label.set('Perdu')
            root.after(2000, root.destroy)
        

root = tk.Tk()

frame = tk.Frame()
txt_label = tk.StringVar()
txt_label.set( 'Voici le jeu du mastermind')
label = tk.Label(root, textvariable=txt_label)
label.pack(padx = 10, pady = 20)
txt_deux_label = tk.StringVar()
txt_deux_label.set('')
label_deux = tk.Label(root, textvariable=txt_deux_label)
label_deux.pack(padx = 10, pady = 20)
couleurs = ['rouge', 'vert', 'jaune', 'bleu', 'violet', 'rose']
positions = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]]
for u in range (6):
    pos = positions[u]
    tk.Button(frame, text = couleurs[u] ,height=2, width=10, command = lambda c = couleurs[u]: afficher_texte(c)
).grid(column=pos[0], row=pos[1], padx=5, pady = 5)


largeur = 300 # taille de la fenetre
hauteur = 350

screen_largeur = root.winfo_screenwidth()
screen_hauteur = root.winfo_screenheight()

x = (screen_largeur // 2) - (largeur // 2)
y = (screen_hauteur // 2) - (hauteur // 2)

root.geometry(f"{largeur}x{hauteur}+{x}+{y}") # Definit la taille de la fenetre et empeche sa modification
root.resizable(False, False)
frame.pack()
root.mainloop()



