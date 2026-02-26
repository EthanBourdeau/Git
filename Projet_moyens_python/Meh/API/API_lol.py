import requests
import json
import os

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

api_url = "https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_7544434805?api_key=RGAPI-ecd998fa-d83f-42af-af08-61629cc245ef"
resp = requests.get(api_url)
match_data = resp.json()

sauvegarde_donnees_json('Data_masster_lol.json', match_data)
