import requests
import os
import json
"""
url = "https://api.hypixel.net/skyblock/bazaar"
response = requests.get(url)
data = response.json()

"""
# Exemple : afficher le prix d'achat d'un Summoning Eye
"""
eye_data = data['products']['SUMMONING_EYE']
print("Prix d'achat :", eye_data['quick_status']['buyPrice'])
"""

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


liste_produits = recuperation_donnees_json('Donnees_prix_hypixel')
"""
for i in liste_produits["products"].values() :
    del i["sell_summary"]
    del i["buy_summary"]
"""
"""
for i in liste_produits["products"].values():
    i['quick_status']['sellPrice'], i['quick_status']['buyPrice'] = round(i['quick_status']['sellPrice'], 2), round(i['quick_status']['buyPrice'], 2)
"""
dico_in = []
for i in liste_produits['products'].values() :
    if i['quick_status']['sellPrice'] != 0 and i['quick_status']['sellPrice'] > 1000000 and i['quick_status']['sellPrice']*i['quick_status']['sellVolume'] > 50000000000:
        dico_in.append({ i['product_id'] :i['quick_status']['buyPrice'] / i['quick_status']['sellPrice'] - 1})

for u in sorted(dico_in, key=lambda d: list(d.values())[0], reverse=True):
    print(u)

#print(sorted([(i['quick_status']['buyPrice'] / i['quick_status']['sellPrice']) - 1 for i in liste_produits['products'].values() if i['quick_status']['sellPrice'] != 0 and i['quick_status']['sellPrice'] > 100000], reverse = True))