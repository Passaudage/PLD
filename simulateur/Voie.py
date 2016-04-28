import Vehicule
import Coordonnees

class Voie:
    def __init__(self, troncon, coordonnees_debut, coordonnees_fin, directions, trajectoire, proba_entree, proba_dir):
        self.intersectionsAccessibles = []
        self.troncon = troncon
        self.coordonnees_debut = coordonnees_debut
        self.coordonnees_fin = coordonnees_fin
        self.vehicules = []
        self.trajectoire = trajectoire
        self.directions = directions
        self.proba_entree = proba_entree
        self.proba_dir = proba_dir

    def creer_vehicule(self, discourtois, longueur):
        prochaine_direction = "droite"
        clio = Vehicule.Vehicule(50, Coordonnees.Coordonnees(0,0), discourtois, longueur, self, prochaine_direction, self.trajectoire, None)
        self.ajouter_vehicule(self)
        dernier_vehicule = self.dernier_vehicule()
        clio.greffe_arbre(dernier_vehicule)

    def direction_possible(self, direction):
        return (direction in self.directions)

    def mise_a_jour_controle_acces(self, temps, simulation_manager):
         self.controleur_acces.notifie_temps(self, temps, simulation_manager)


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