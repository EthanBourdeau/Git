import random
from tkinter import *
import time
from pathlib import Path

"""
Setup des equipes
"""
def creer_joueur(nom,poste, vitesse, precision, force) :
    return {"nom" : nom,"poste" : poste, "vitesse" : vitesse, "precision" : precision, "force" : force, "blessure": "aucune", 'his': []}

def creer_equipe(nom):
    return {"nom" : nom,"joueurs" : [], "score" : 0,"victoires" : 0,"vif" : False}

def ajouter_joueurs(equipe):
    roles = ['Attrapeur', 'Gardien', 'Batteur', 'Batteur', 'Poursuiveur','Poursuiveur','Poursuiveur']
    for u in range (len(roles)) :
        joueur = creer_joueur(determ_nom(), roles[u], random.randint(0, 100), random.randint(1, 20), random.randint(0, 10))
        equipe["joueurs"].append(joueur)
    return equipe

def determ_nom ():
    f = open("Prenoms.txt", "r")
    pr = f.readlines()
    nom_choisi = pr[random.randint(0, len(pr)  - 1)]  
    print(len(pr))
    nom_trad = trad_carac(nom_choisi) 
    return nom_trad

def trad_carac (trad):
    carac_spe = ["Ã©","Ã¨","Ã«","Ã§","\n"]
    corres = ["é","è","ë","ç"," "]
    for i in range (len(corres)):
        trad = trad.replace(carac_spe[i], corres[i])
    return trad

"""
Déroulement manche
"""

def action_joueur  (equipe, fatigue, i)  :
    if equipe["joueurs"][i]["blessure"] == "aucune" or equipe["joueurs"][i]["blessure"] == 0:

        proba_fatigue = round((fatigue / (fatigue+ equipe["joueurs"][i]['force']**1.3 +2)) * 100, 1)
        a = random.randint(0,100)
        if a < proba_fatigue :
            equipe["joueurs"][i]['his'].append("trop fatigué, il est tombé") 
            return "trop fatigué, il est tombé"

        elif equipe["joueurs"][i]["poste"] == "Poursuiveur" :
            precision = random.randint (1, 20)
            if precision < equipe["joueurs"][i]["precision"]:
                equipe["joueurs"][i]['his'].append("marque son but !")
                return "marque son but !"
            else :
                equipe["joueurs"][i]['his'].append("raté son tir")
                return "raté son tir"
            
        elif equipe["joueurs"][i]["poste"] == "Attrapeur" :
            P = random.random()*100
            if P <((equipe["joueurs"][i]["precision"]/20)*(equipe["joueurs"][i]["vitesse"]/100)* 10): 
                equipe["vif"] = True
                equipe["joueurs"][i]['his'].append("attrape le vif d'or")
                return "attrape le vif d'or"
            else :
                equipe["joueurs"][i]['his'].append("rate le vif d'or")
                return "rate le vif d'or"
        
        else :
            equipe["joueurs"][i]['his'].append('defend')
            return "defend"
    else :

        equipe["joueurs"][i]['his'].append("joueurs bléssé, passe son tour")
        return "joueurs bléssé, passe son tour"

"""
Météo
"""

def générer_météo():
    conditions = ["soleil", "orage", "vent", "brume"]
    return random.choice(conditions)

"""
Blessures
"""

def générer_blessures(meteo):
    p_bless = {"soleil" : 0.05, "orage" : 0.1, "vent": 0.1, "brume" : 0.1}
    grav_bless = {"soleil" : [0.2, 0.5], "orage" : [0.3, 0.7], "vent" : [0.2, 0.5], "brume" : [0.3, 0.7]}

    r= random.random()
    if r < p_bless[meteo]:
        det_bl = random.random()
        if det_bl < grav_bless[meteo][0]:
            return "out"
        if grav_bless[meteo][0] <= det_bl < grav_bless[meteo][1]:
            return 5
        if grav_bless[meteo][1] <= det_bl:
            return 2
    return "aucune"

def gerer_blessure (team, i, meteo):
    y = team['joueurs'][i]['blessure']

    if  meteo == "orage":
        if random.random() < 0.05:
            y = 'out'
    if y == "aucune":
        y = générer_blessures(meteo)
    else:
        if y == 0:
            y = "aucune"
        elif y== "out":
            y = "out"
        else :          
            y =y - 1
    return team
"""
C du tkinter tkt
"""   

def afficher_selection(boite, nv_f):
    selection = boite.curselection()
    if selection:
        valeur = boite.get(selection[0])
        boite.delete(0, END)
        for b in nv_f:
            if b['nom'] + "(" + b['poste'] +")" == valeur:
                for g in range (len(b['his'])):
                    boite.insert(END, 'Tour '+ str(g+1) +' :')
                    boite.insert (END, b['his'][g])

def affiche_joueurs(boite, eqs):
    boite.delete(0, END)
    tc = 0
    for i in eqs :
        tc = tc + 1
        boite.insert(END,"Equipe " + str(tc) + " :")
        for u in i['joueurs']:
            boite.insert (END, str(u['nom']) + "(" + u['poste'] +")")


def affiche_stats_tkinter(eqs):

    #Converrtis les stats finales en nu format plus facile a interpreter (tkt touche a r)
    nv_f =  []
    for h in eqs:
        for d in h['joueurs']:
            nv_f.append(d)

    # Initialiser la fenêtre principale
    fenetre = Tk()
    fenetre.title("Jeu de clic")

    largeur_fenetre = 1080
    hauteur_fenetre = 720

    fenetre.minsize(largeur_fenetre, hauteur_fenetre)
    fenetre.config(background = '#3199ba')

    # Obtenir la taille de l'écran
    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()

    # Calculer les coordonnées x et y pour centrer la fenêtre
    x = (largeur_ecran - largeur_fenetre) // 2
    y = (hauteur_ecran - hauteur_fenetre) // 2

    # Positionner la fenêtre
    fenetre.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{x}+{y}")



    # Frame
    frame = Frame(fenetre, bg = '#3199ba')

    # gauche frame
    gauche_frame = Frame(frame, bg = '#3199ba')

    # droite frame
    droite_frame = Frame(frame, bg = '#3199ba')

    # Label
    label = Label(gauche_frame, text='Choisi qlqn', font = ('Courriel',17), bg ='#3199ba', fg = 'white', width=16 )
    label.pack(pady = 50)


    # List box
    boite = Listbox(droite_frame, width=70, height = 28, font = ('Arial', 15))
    boite.pack()
    affiche_joueurs(boite, eqs)

    # Agence tt ce beau monde
    droite_frame.grid(row = 0, column = 1, sticky = "w", padx = 20)
    gauche_frame.grid(row = 0, column = 0, sticky = "w",padx = 20) 
    frame.pack(expand = 'yes')

    # Bouton
    bout = Button(gauche_frame, text='Voir les stats du joueur', width= 20, height=2, command = lambda : afficher_selection(boite, nv_f))
    bout.pack(fill = "x")

    dx_btn = Button(gauche_frame, text="Retour aux joueurs",width= 20, height=2, command=lambda :  affiche_joueurs(boite, eqs))
    dx_btn.pack(fill = "x", pady = 10 )
    # Lancer le jeu
    fenetre.mainloop()


"""
Programme principal
"""

def maj_scores (equipes, res, w):
    if res == "marque son but !":
        equipes[w]["score"] =equipes [w]["score"] + 10 
    if res == "attrape le vif d'or":
        equipes[w]["score"] = equipes[w]["score"] + 60
    return equipes

def affiche_score (eq):
    res = []
    for g in eq:
        res.append(g['score'])
    print("Le score est de " + str(res))
        
def aff_gag ( q):
    max = 0
    for k in range(len(q)):
        if q[k]['score'] > q[max]['score']:
            max = k 
    print("L'équipe " + str(max + 1) + " à gagné")
    return None

def verif_vif(eq):
    for y in eq :
        if y['vif'] == True :
            return True
    return False

def simuler_match():
    n_eqs = ["gryfondor", "serpentar", "poufsouffle","serdaigle"]
    temps = 20
    fatigue = 0
    nbr_eqs = int(input("Combien d'équipes"))
    if nbr_eqs > 4 or nbr_eqs <= 1 :
        print("Nombre d'equipes invalide")
        return None
    
    else :
        eqs  = []
        for f in range (nbr_eqs):
            eqs.append(ajouter_joueurs(creer_equipe(n_eqs[f])))

    while (verif_vif(eqs) == False) and temps > 1:
        print(" ")
        tour = 21 - temps
        print("Tour " + str(tour) + ":")
        print("")
        meteo = générer_météo()
        for w in range (len(eqs)): # Autrement dit : pour toutes les equipes
            for i in range (len(eqs[w]['joueurs'])): # Autrement dit : repete autant de fois qu'il y a des joueurs dns l'equipe
                eqs[w] = gerer_blessure(eqs[w], i, meteo) # Génére une blesure (peut etre), si il est deja, reduit son tp de blessure
                res_tour = action_joueur(eqs[w], fatigue, i) # Avec une equipe, simule une manche et recupere les actions de chasue joueurs
                print(res_tour) # Afiche le resulats de la simulation
                eqs = maj_scores(eqs, res_tour, w) # Mise a jour du score de l'equipe
            print("")
        fatigue = fatigue + 0.25 # Augmente la fatigue générale
        temps = temps -1 # Fait passer le temps
        affiche_score(eqs) # Affiche le score
    aff_gag(eqs)
    affiche_stats_tkinter(eqs)
    
    return 



simuler_match()
