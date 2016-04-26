from enum import Enum

import coordonnees
import controleAcces
import vehicule
    

class voie:
    def __init__(self, direction, controleur_acces, troncon, feu, coordonnees_debut, coordonnees_fin):
        self.intersectionsAccessibles = []
        self.direction = direction
        self.controleur_acces = controleur_acces
        self.troncon = troncon
        self.coordonnees_debut = coordonnees_debut
        self.coordonnees_fin = coordonnees_fin


    def mise_a_jour_controle_acces(self, temps, simulation_manager):
         self.controleur_acces.notifie_temps(self, temps, simulation_manager)

    def get_controleur_acces(self):
        return self.controleur_acces





    def setTroncon(self, troncon):
        self.troncon = troncon

class troncon:
    def __init__(self, tete, queue, probabilite_entree, longueur, coordonnees_):
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


    """
    ainsi toujours poussé vers de nouveaux rivages
    dans la nuit éternelle emporté sans retour
    ne pourrons nous jamais sur l'océan des ages
    jetez l'ancre un seul jour ?
        AdL
    """