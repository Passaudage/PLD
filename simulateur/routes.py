from enum import Enum

import coordonnees
import controleAcces
import vehicule


class intersection:
    

class voie:
    def __init__(self, direction):
        self.intersectionsAccessibles = []
        self.direction = direction
        self.vehicules = []

    def a_de_la_place(self):
        return

    def setTroncon(self, troncon):
        self.troncon = troncon

class troncon:
    def __init__(self, tete, queue, probabilite_entree, longueur):
        self.tete = tete
        self.queue = queue
        self.probabilite_entree = probabilite_entree
        self.longueur = longueur
        self.voies = []

class direction(Enum):
    gauche = 1
    tout_droit = 2
    droite = 3