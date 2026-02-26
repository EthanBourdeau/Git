import tkinter as tk
import random

def gener_seq():
    couleurs = ['rouge', 'vert', 'jaune', 'bleu', 'violet', 'rose']
    return [random.choice(couleurs) for _ in range(4)]

vies_joueur = 10
sequence = gener_seq()

def verif_reponse(reponse, joueur):
    comparaison = []
    for m in range(4):
        if reponse[m] == joueur[m]:
            comparaison.append('Correct')
        elif joueur[m] in reponse:
            comparaison.append('Mal placé')
        else:
            comparaison.append('Mauvais')
    return comparaison

def afficher_cercles(liste_couleurs):
    canvas_deux.delete("all")
    couleur_map = {
        'rouge': '#FF4C4C',
        'vert': '#4CAF50',
        'jaune': '#FFEB3B',
        'bleu': '#2196F3',
        'violet': '#9C27B0',
        'rose': '#F48FB1'
    }
    for i, couleur in enumerate(liste_couleurs):
        x = 20 + i * 65
        canvas_deux.create_oval(x, 10, x + 40, 50, fill=couleur_map.get(couleur, 'white'), outline='black')

def afficher_texte(couleur):
    ref = ['rouge', 'vert', 'jaune', 'bleu', 'violet', 'rose']
    texte_actu = txt_label.get()
    if len(texte_actu.split()) == 4 or texte_actu.split()[0] not in ref:
        texte_actu = ''
    txt_label.set(texte_actu + ' ' + couleur)
    if len(txt_label.get().split()) == 4:
        liste = txt_label.get().split()
        afficher_cercles(liste)
    verif_taille()

def verif_taille():
    global vies_joueur, sequence
    msg_affich = txt_label.get()
    if len(msg_affich.split()) == 4:
        infos_joueur = msg_affich.split()
        if infos_joueur == sequence:
            txt_label.set('Bien joué')
            root.after(2000, root.destroy)
        else:
            nouveau_message = ' '.join(verif_reponse(sequence, infos_joueur))
            txt_label.set(nouveau_message)
        vies_joueur -= 1
        if vies_joueur == 0:
            txt_label.set('Perdu')
            root.after(2000, root.destroy)

root = tk.Tk()
root.title("Mastermind Couleurs")
root.configure(bg='#494FAB')

frame = tk.Frame(bg="#494FAB")

txt_label = tk.StringVar()
txt_label.set('Voici le jeu du mastermind')
label = tk.Label(root, textvariable=txt_label, bg="#787ED4", font=('Helvetica', 12), fg='white')
label.pack(padx=10, pady=20, fill='both')

# Canvas pour les cercles
canvas_deux = tk.Canvas(root, width=280, height=60, bg="#787ED4", highlightthickness=0)
canvas_deux.pack(padx=10, pady=10)

# Boutons 

couleurs = ['rouge', 'vert', 'jaune', 'bleu', 'violet', 'rose']
positions = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]

def style_bouton(widget):
    widget.configure(
        bg="#6C70D4",
        fg="white",
        activebackground="#5054A0",
        activeforeground="white",
        font=('Helvetica', 11, 'bold'),
        relief="raised",
        bd=3,
        cursor="hand2"
    )

for u in range(6):
    pos = positions[u]
    bouton = tk.Button(frame,
                       text=couleurs[u],
                       height=2,
                       width=10,
                       command=lambda c=couleurs[u]: afficher_texte(c))
    style_bouton(bouton)
    bouton.grid(column=pos[0], row=pos[1], padx=8, pady=8)


largeur = 300
hauteur = 400
screen_largeur = root.winfo_screenwidth()
screen_hauteur = root.winfo_screenheight()
x = (screen_largeur // 2) - (largeur // 2)
y = (screen_hauteur // 2) - (hauteur // 2)
root.geometry(f"{largeur}x{hauteur}+{x}+{y}")
root.resizable(False, False)

frame.pack(pady=15)
root.mainloop()

#python -m PyInstaller --onefile --windowed Mastermind_python.p