import random

def melange_faro(liste, liste1 = [], liste2 = []):
    if len(liste) == 0:
        return melange(liste1, liste2)  

    else:
        liste1.append(liste[0])
        liste2.append(liste[1])
        return melange_faro(liste[2:],  liste1, liste2)

def melange(liste1, liste2):
    if len(liste1) == 0 or len(liste2) == 0:
        return liste1 + liste2
    else:
        bloc = [liste1[len(liste1)- 1]] + [liste2[len(liste2)- 1]]
        return bloc + melange(liste1[:len(liste1)- 1], liste2[:len(liste2) - 1])
    

liste_pre_m = list(range(10))
print(liste_pre_m)
print(melange_faro(liste_pre_m))