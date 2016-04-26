from enum import Enum

import coordonnees
import controleAcces
import vehicule
    

class voie:
    def __init__(self, direction, controleur_acces, troncon):
        self.intersectionsAccessibles = []
        self.direction = direction
        self.controleur_acces = controleur_acces
        self.troncon = troncon

    def mise_a_jour_controle_acces(self, temps, simulation_manager):
         self.controleur_acces.notifie_temps(self, temps, simulation_manager)

    def get_controleur_acces(self):
        return self.controleur_acces

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

    #trouver voie avec bonne direction

class direction(Enum):
    gauche = 1
    tout_droit = 2
    droite = 3