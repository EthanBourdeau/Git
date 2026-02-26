import random

"""
Creer un module avec la classe jeu_carte qui genere les 52 cartes avec 
piocher() : sort une carte du jeu aleatoiremant
melanger():

"""

couleurs = ['pique', 'coeur', 'trefle', 'carreau']
figures = ['as', '2', '3', '4','5', '6', '7', '8', '9', '10', 'valet', 'dame', 'roi']

class Jeu_carte :
    def __init__(self):
        self.jeu_cartes = []
        for col in couleurs :
            for fig  in figures:
                self.jeu_cartes.append(f'{fig} de {col}')

    def melanger (self):
        random.shuffle(self.jeu_cartes)
        print(len(self.jeu_cartes))

    def piocher(self):

        if len(self.jeu_cartes) == 0:
            raise ValueError ('Le jeu de carte est vide')
        
        a = random.choice(range(len(self.jeu_cartes)))
        carte_retour  = (self.jeu_cartes[a])
        self.jeu_cartes.remove(carte_retour)
        return carte_retour

    def __str__(self):
        return f'{self.jeu_cartes['figure']} de {self.jeu_cartes['couleur']}'

jc = Jeu_carte()

print(jc.jeu_cartes)

carte = jc.piocher()
jc.melanger()

print(jc.jeu_cartes)
print(carte)



