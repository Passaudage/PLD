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
        prochaine_direction = self.directions[0]

        dernier_vehicule = self.dernier_vehicule()
        clio = Vehicule.Vehicule(simulateur, discourtois, longueur, self, prochaine_direction, self.coordonnees_debut, self.coordonnees_fin, self.orientation, dernier_vehicule)
        self.ajouter_vehicule(clio)

    def direction_possible(self, direction):
        return (direction in self.directions)

    """set de direction et probabilité de prendre cette direction en fonction des troncons accessibles et de leur proba """

    def ajouter_vehicule(self, vehicule):
        self.vehicules.append(vehicule)

    def ajouter_vehicule_avant(self, second_vehicule, premier_vehicule):
        self.vehicules.insert(self.vehicules.index(premier_vehicule)+1, second_vehicule)
        
    def ajouter_vehicule_destination(self, vehicule):
        for v in self.vehicules:
            # si v est en train d'arriver
            if(v.nouvelle_voie==self):
                #si v va arriver plus loin
                if(abs(v.destination-self.coordonnees_debut)+1 >= abs(vehicule.destination-self.coordonnees_debut)):
                    pass
                #si v va arrive derrière et qu'on est déjà devant, on met vehicule juste devant dans la liste
                elif (abs(v.coordonnees-self.coordonnees_debut) < abs(vehicule.coordonnees-self.coordonnees_debut)):
                    self.vehicules.insert(self.vehicules.index(v), vehicule)
                    return
            # si v est devant le point d'entrée de vehicule
            elif(abs(v.coordonnees-self.coordonnees_debut)+1 >= abs(vehicule.destination-(self.orientation*vehicule.longueur*2)-self.coordonnees_debut)):
                pass
            # si v est derrière, on met vehicule juste devant dans la liste
            else:
                self.vehicules.insert(self.vehicules.index(v), vehicule)
                return
        self.ajouter_vehicule(vehicule)
        
    def connait(self,vehicule):
        return any(v == vehicule for v in self.vehicules)
                

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
            return self.vehicules[self.vehicules.index(vehicule)-1]

    def est_passant(self, direction):
        return self.troncon.est_passant(direction, self.sens)

    def get_proba_voie(self):
        return self.troncon.get_proba_situation_voie(self, self.directions)

    def demander_intersection(self):
        return self.troncon.get_intersection(self)

    def __eq__(self, other):
        return (self.coordonnees_debut == other.coordonnees_debut) and (self.coordonnees_fin == other.coordonnees_fin)

    def get_vehicules(self):
        vehicules = []
        for vehicule in self.vehicules:
            if (vehicule.voie == self):
                vehicules.append(vehicule)
        return vehicules

