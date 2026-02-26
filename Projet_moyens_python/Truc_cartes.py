import random
import tkinter as tk
import matplotlib.pyplot as plt
def sim_tirage():
    r = round(100*random.random(), 2)
    if r >= 0 and r < 48.8:
        return 5
    elif r >= 48.8 and r < (48.8 + 28):
        return 2
    elif r >= (48.8 + 28) and r < (48.8 + 28 + 10):
        return 10
    elif r >= (48.8 + 28 + 10) and r < (48.8 + 28 + 10 + 1.4):
        return 25
    elif r >= (48.8 + 28 + 10 + 1.4) and r < (48.8 + 28 + 10 + 1.4+ 0.5):
        return 50
    elif r >= (48.8 + 28 + 10 + 1.4+ 0.5) and r < (48.8 + 28 + 10 + 1.4+ 0.5+0.2):
        return 100
    else:
        return 0

def sim_tour(nbr_rp):
    nbr_invoq = nbr_rp//400
    ret = 0
    for i in range(nbr_invoq):
        ret += sim_tirage()
    return ret  

def sim_mult(nbr_rp):
    val_his = 0
    for i in range(10000):
        val_his += sim_tour(nbr_rp)
    return val_his/10000

def gen_g():
    vr = [100 * i for i in range(60)]
    print(vr)
    rr = [sim_mult(100*i) for i in range(60)]
    print(rr)
    plt.figure(figsize=(8, 5))
    plt.plot(vr, rr, marker="o")
    plt.title("Évolution de la population")
    plt.xlabel("Année")
    plt.ylabel("Population ")
    plt.grid(True)
    plt.show()

root = tk.Tk()
root.title("Simulation de l'évolution de la population")
root.geometry("500x400")

tk.Label(root, text="Nombre de RP dont tu disposes :").pack()
nb_rp = tk.Entry(root)
nb_rp.pack()
nb_rp.insert(0, "2000")

tk.Label(root, text="Combien d'ES vises tu:").pack()
nb_es = tk.Entry(root)
nb_es.pack()
nb_es.insert(0, "40")

"""
tk.Label(root, text="Pas (en années) :").pack()
entry_pas = tk.Entry(root)
entry_pas.pack()
entry_pas.insert(0, "1")


tk.Label(root, text="Variations relatives (en %) (séparées par des virgules) :").pack()
entry_vr = tk.Entry(root)
entry_vr.pack()
entry_vr.insert(0, "2.5")

tk.Label(root, text="Année maximale :").pack()
entry_am = tk.Entry(root)
entry_am.pack()
entry_am.insert(0, "2050")
"""

tk.Button(root, text="Lancer la simulation", command= lambda : sim_mult(int(nb_rp.get()), int(nb_es.get())), bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(root, text="Graphe", command= gen_g, bg="#4CAF50", fg="white").pack(pady=10)
root.mainloop()