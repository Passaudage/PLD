import math

import coordonnees
import feu
import vehicule


class voie:
    def __init__(self, direction, controleur_acces, troncon, feu, coordonnees_debut, coordonnees_fin):
        self.intersectionsAccessibles = []
        self.controleur_acces = controleur_acces
        self.troncon = troncon
        self.coordonnees_debut = coordonnees_debut
        self.coordonnees_fin = coordonnees_fin
        self.vehicules = []
        self.trajectoire = self.calculer_trajectoire()
        self.directions = set()

    def creer_vehicule(self, discourtois, longueur):
        prochaine_direction = "droite"
        trajectoire = self.calculer_trajectoire(self)
        clio = vehicule(50, coordonnees(0,0), discourtois, longueur, self, prochaine_direction, None)
        self.ajouter_vehicule(self)
        dernier_vehicule = self.dernier_vehicule()
        clio.greffe_arbre(dernier_vehicule)

    def direction_possible(self, direction):
        return (direction in self.directions)

    def mise_a_jour_controle_acces(self, temps, simulation_manager):
         self.controleur_acces.notifie_temps(self, temps, simulation_manager)

    def get_controleur_acces(self):
        return self.controleur_acces

    #trajectoire : coordonees vecteur norme 1
    def calculer_trajectoire(self):
        norme = math.sqrt((self.coordonnees_fin.x-self.coordonnees_debut.x)**2 + (self.coordonnees_fin.y-self.coordonnees_debut.y)**2)
        return coordonnees((self.coordonnees_fin.x-self.coordonnees_debut.x)/norme, (self.coordonnees_fin.y-self.coordonnees_debut.y)/norme)

    """set de direction et probabilité de prendre cette direction en fonction des troncons accessibles et de leur proba """

    def ajouter_vehicule(self, vehicule):
        self.vehicules.append(vehicule)

    #notification du véhicule en tête qui s'en va

    def supprimer_vehicule(self, vehicule):
        self.vehicules.delete(vehicule)

    def dernier_vehicule(self):
        return self.vehicules(-1)

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
    def trouver_voie_direction(self, direction):
        voies_possibles = []
        for voie in self.voies:
            if(voie.direction_possible(direction)):
                voies_possibles.append(voie)
        return voies_possibles

    """
    ainsi toujours poussé vers de nouveaux rivages
    dans la nuit éternelle emporté sans retour
    ne pourrons nous jamais sur l'océan des ages
    jetez l'ancre un seul jour ?
        AdL
    """
