import Vehicule
import Coordonnees

class Voie:

    def __init__(self, troncon, coordonnees_debut, coordonnees_fin, directions, proba_entree, proba_dir, vitesse_max):
        self.intersectionsAccessibles = []
        self.troncon = troncon
        self.coordonnees_debut = coordonnees_debut
        self.coordonnees_fin = coordonnees_fin
        self.vehicules = []
        self.orientation = (coordonnees_fin-coordonnees_debut).normaliser()
        self.directions = directions
        self.proba_entree = proba_entree
        self.proba_dir = proba_dir
        self.vitesse_max = vitesse_max

    def creer_vehicule(self, simulateur, discourtois, longueur):
        prochaine_direction = "droite"

        clio = Vehicule.Vehicule(simulateur, discourtois, Coordonnees.Coordonnees(0,0), longueur, self, prochaine_direction, self.coordonnees_debut, self.coordonnees_fin, self.orientation, None)
        self.ajouter_vehicule(clio)
        dernier_vehicule = self.dernier_vehicule()
        clio.greffe_arbre(dernier_vehicule)

    def direction_possible(self, direction):
        return (direction in self.directions)

    """set de direction et probabilité de prendre cette direction en fonction des troncons accessibles et de leur proba """

    def ajouter_vehicule(self, vehicule):
        self.vehicules.append(vehicule)

    def ajouter_vehicule_avant(self, second_vehicule, premier_vehicule):
        self.vehicules.insert(self.vehicules.index(premier_vehicule)+1, second_vehicule)

    #notification du véhicule en tête qui s'en va

    def supprimer_vehicule(self, vehicule):
        self.vehicules.remove(vehicule)

    def dernier_vehicule(self):
        return self.vehicules[-1]

    def setTroncon(self, troncon):
        self.troncon = troncon

    def precedent(self, vehicule):
        if(self.vehicules.index(vehicule)==0):
            return None
        else:
            return self.vehicules.index(vehicule)-1

    def est_passant(self, direction):
        return self.troncon.getFeu(direction).est_passant()

    def get_proba_dir(self, direction):
        return self.proba_dir.get(direction)

    def demander_intersection(self):
        return self.troncon.get_intersection(self)
