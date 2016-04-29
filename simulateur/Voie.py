import Vehicule
import Coordonnees

class Voie:

    def __init__(self, troncon, coordonnees_debut, coordonnees_fin, directions, vitesse_max, sens):
        self.intersectionsAccessibles = []
        self.troncon = troncon
        self.coordonnees_debut = coordonnees_debut
        self.coordonnees_fin = coordonnees_fin
        self.vehicules = []
        self.orientation = (coordonnees_fin-coordonnees_debut).normaliser()
        self.directions = directions
        self.vitesse_max = vitesse_max
        self.sens = sens

    def creer_vehicule(self, simulateur, discourtois, longueur):
        prochaine_direction = "droite"

        dernier_vehicule = self.dernier_vehicule()
        clio = Vehicule.Vehicule(simulateur, discourtois, Coordonnees.Coordonnees(0,0), longueur, self, prochaine_direction, self.coordonnees_debut, self.coordonnees_fin, self.orientation, dernier_vehicule)
        self.ajouter_vehicule(clio)

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
		if(self.vehicules):
			return self.vehicules[-1]
		else:
			return None

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

    def get_proba_voie(self):
        return self.troncon.get_proba_situation_voie(self, self.directions)

    def demander_intersection(self):
        return self.troncon.get_intersection(self)
