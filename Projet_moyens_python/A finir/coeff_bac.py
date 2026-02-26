import tkinter as tk


def interface():
    def get_values():
        liste_val = []
        for i in liste_entrees:
            v = i.get()
            if v == '':
                liste_val.append(0)
            else:
                liste_val.append(int(v))

        print(liste_val)
    root = tk.Tk()
    root.geometry("600x500")
    root.config(bg = "#F7C2C2")
    frame = tk.Frame(root, bg = "#F7C2C2")
    liste_entrees = []

    liste_matieres = ["Spé 1", "SPé 2","Bac de francais Ecrit", "Bac de francais Oral","Epreuve de philosophie", "Grand Oral", "Histoire", "LV 1", "LV2", "EPS (sport terminale)", "ES physique", "ES SVT", "Spé abandonnées en premiere", "EMC"]
    for i in range(14):
        tk.Label(frame, text = liste_matieres[i]).grid(row = i, column=0, pady = 5)
        entree = tk.Entry(frame)
        entree.grid(row = i, column=1, pady = 5)
        liste_entrees.append(entree)
    tk.Button(frame, command = get_values, text = "Calculer mon resultat du bac").grid(row = 14, column=0, ipady = 5)
    frame.pack()
    root.mainloop()

def moyenne(notes):
    coeffs = {"spe1":16, "spe2":16, "fr_e":5, "fr_o":5, "philo":8, "g_oral":10,  "his": 6, "lva":6, "lvb":6, "eps":6, "es_p":3, "es_s":3, "spe_ab":8, "emc":2}
    tot = 0
    for i in coeffs.keys():
        tot += notes[i] * coeffs[i]

    print(tot, tot/100)
    return tot /100

interface()