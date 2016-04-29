import Coordonnees
import Intersection
from math import sqrt
import copy

class Vehicule:
    distance_minimale_roulant = 150 #cm
    distance_minimale = 30 #cm
    proportion_discourtois = 0.8
    acceleration_max = 1 # m.s^(-2)
    deceleration_conf = 3 # m.s^{-2}
    temps_reaction = 1.5 # secondes
    largeur = 170 # cm
    count = 0
    v_max = 50
    liste_voitures = []

    def __init__(self, simulateur, discourtois, longueur, voie, prochaine_direction, origine, destination, direction, vehicule_precedent):
        Vehicule.count += 1
        Vehicule.liste_voitures.append(self)

        #~ print(Vehicule.count)
        self.simulateur = simulateur
        self.coordonnees = copy.deepcopy(origine)
        self.discourtois = discourtois
        self.longueur = longueur
        self.prochaine_direction = prochaine_direction
        self.voie = voie
        self.origine = origine
        self.destination = destination
        self.direction = direction
        self.changer_trajectoire(destination, direction)
        self.vitesse = Coordonnees.Coordonnees(0, 0)
        self.acceleration = Coordonnees.Coordonnees(0, 0)

        # non initialisés
        self.racine = None
        self.nouvelle_voie = None
        self.intersection = None

        # Mise dans l'arbre
        self.vehicule_precedent = vehicule_precedent
        self.vehicules_suivants = []
        if (vehicule_precedent != None):
            self.greffe_arbre(vehicule_precedent)
        else:
            self.racine = self
            # se déclarer tête de liste 
            self.simulateur.add_listener(self)


    def changeDirection(self, x, y):
        self.direction = Coordonnees.Coordonnees(x, y)

    def avancerBoucle(pasTemporel):
        return False

    def notifie_temps(self, nb_increment, simulateur):
        """
            Appelle la méthode d'avancement du véhicule et le transmet aux fils dans l'arbre
                # nb_increment : numéro d'incrément
                # simulateur : impulseur des incréments
                # @author : Marcus
        """
        #print("avant : " + str(self.coordonnees))
        self.avance_vehicule(nb_increment, simulateur.nombre_ticks_seconde)
        if (len(self.vehicules_suivants) == 0):
            #print("après : " + str(self.coordonnees))
            return
        else:
            for vehicule_suivant in self.vehicules_suivants:
                vehicule_suivant.notifie_temps(nb_increment, simulateur)
        #print("après : " + str(self.coordonnees))

    def avance_vehicule(self, incr, nb_tick):
        """
            Réalise les changements de directions, calcule la position de l'obstacle le plus proche, 
            met l'arbre à jour et appelle la méthode qui calcule le chemin
                # incr : numéro d'incrément
                # nb_tick : nombre de ticks par seconde
                # @author : Marcus
        """
        # si on existe pas encore
        if (self.vehicule_precedent is not None and self.vehicule_precedent.coordonnees == self.coordonnees):
            #print("Je n'existe pas")
            return

        # Si il faut changer de voie
        if (not self.voie.direction_possible(self.prochaine_direction)):
            #print("Ma voie est " + str(self.voie))
            self.nouvelle_voie = self.voie.troncon.trouver_voie_direction(self.prochaine_direction, self.voie.sens)[0]
            direction_virage = self.nouvelle_voie.coordonnees_debut - self.voie.coordonnees_debut
            distance_avant = self.direction * 2
            trajet = direction_virage + distance_avant
            self.destination = trajet + self.coordonnees

        # Si on a dépassé la destination (arrivée sur intersection ou nouvelle_voie)
        if ((self.coordonnees - self.destination) * self.direction >= 0):

            # sortie de l'intersection
            if (self.intersection is not None):
                self.voie = self.nouvelle_voie
                self.nouvelle_voie = None
                self.voie.ajouter_vehicule(self)
                self.intersection.retirer_vehicule(self)
                self.intersection = None

                self.prochaine_direction = "D"
                self.direction = self.voie.orientation
                self.changer_trajectoire(self.destination, self.orientation_cible)
            # arrivée sur intersection
            elif (self.nouvelle_voie is None):
                self.intersection = self.voie.demander_intersection()
                self.intersection.ajouter_vehicule(self)
                self.voie.supprimer_vehicule(self)

                self.nouvelle_voie = self.intersection.demander_voies_sorties(self.voie, self.prochaine_direction)
                self.changer_trajectoire(self.destination, self.orientation_cible)
            # fin de changement de voie
            else:
                self.voie.supprimer_vehicule(self)
                self.nouvelle_voie.ajouter_vehicule_avant(self, self.vehicule_precedent)
                self.voie = self.nouvelle_voie

                self.nouvelle_voie = None
                self.direction = self.voie.direction
                self.changer_trajectoire(self.destination, self.orientation_cible)

        coordonnees_obstacle = None
        (coordonnees_obstacle, vehicule_blocant) = self.trouver_obstacle()

        
        # si l'obstacle est un feu rouge
        if (vehicule_blocant == "feu"):
            self.mettre_coordonnees_a_jour(incr, nb_tick, Coordonnees.Coordonnees(0,0), coordonnees_obstacle)
            return
        # Si l'obstacle est un véhicule, on met éventuellement l'arbre à jour
        #aucun obstacle
        if (vehicule_blocant is None):
            self.decrochage_arbre()
            self.mettre_coordonnees_a_jour(incr, nb_tick, None, None)
        #nouvel obstacle
        elif (self.vehicule_precedent != vehicule_blocant):
            self.change_arbre(vehicule_blocant)
            self.mettre_coordonnees_a_jour(incr, nb_tick, vehicule_blocant.vitesse, coordonnees_obstacle)
            

    def trouver_obstacle(self):
        """
            Calcule l'obstacle le plus proche dans la direction actuelle
                # @author : Marcus
        """
        # si on est sur une intersection
        if (self.intersection is not None):
            return self.intersection.donner_obstacle(self.coordonnees, self.direction)

        # si on est en changement de voie
        elif (not self.voie.direction_possible(self.prochaine_direction)):
            x = None
            y = None
            bv = None
            av = None
            ac = None
            bc = None 
            if (self.direction.x == 0):
                x = self.coordonnees.x
            else:
                av = self.direction.y / self.direction.x
                bv = self.coordonnees.y - av * self.coordonnees.x
            if(self.nouvelle_voie.orientation.x == 0):
                x = self.nouvelle_voie.coordonnees_debut.x
            else:
                ac = self.nouvelle_voie.orientation.y / self.nouvelle_voie.orientation.x
                bc = self.nouvelle_voie.coordonnees_debut.y - ac * self.nouvelle_voie.coordonnees_debut.x
            if(x is None):
                x = (bv - bc) / (ac - av)
            if(self.direction.x != 0):
                y = av * x + bv
            elif(self.nouvelle_voie.orientation.x != 0):
                y = ac * x + bc
            else:
                pass
            p = Coordonnees.Coordonnees(x, y)
            for vehicule in self.nouvelle_voie.vehicules:           
                # si l'arrière du véhicule est devant le point d'insertion voulu, on passe
                if (abs(vehicule.donner_arriere() - self.nouvelle_voie.coordonnees_debut)
                        > abs(p - self.nouvelle_voie.coordonnees_debut)):
                    pass

                # si un véhicule gêne
                elif (abs(vehicule.coordonnees - vehicule.voie.coordonnees_debut)
                          > abs(p - self.nouvelle_voie.coordonnees_debut)):
                    return (p, vehicule)

                else:
                    return (None, None)

        # s'il y a qqun devant sur la voie
        elif (self.voie.precedent(self) is not None):
            vehicule_devant = self.voie.precedent(self)
            arriere_vehicule = (vehicule_devant.coordonnees - self.direction * self.longueur)
            return (arriere_vehicule, vehicule_devant)

        # si on est devant
        else:
            # feu_vert
            if (self.voie.est_passant(self.prochaine_direction)):
                print("yolo")
                intersection = self.voie.demander_intersection()
                return intersection.donner_obstacle(self.coordonnees, self.direction)
            # feu_rouge
            else:
                return (self.destination, "feu")


    # S'ajouter en feuille sur un arbre
    def greffe_arbre(self, vehicule_precedent):
        """
            S'accroche à un arbre à partir d'un élément
                # vehicule_precedent : vehicule sur lequel on s'attache
                # @author : Marcus
        """
        if (vehicule_precedent.racine == self.racine):
            return
        if(self.racine == self):
            self.simulateur.del_listener(self)
        self.set_vehicule_precedent(vehicule_precedent)
        vehicule_precedent.add_vehicule_suivant(self)
        self.propager_racine(vehicule_precedent.racine)
        
    def decrochage_arbre(self):
        """
            Se décroche de son arbre et donne l'information aux fils
                # @author : Marcus
        """
        if (self.vehicule_precedent is None):
            return
        self.simulateur.add_listener(self)
        self.vehicule_precedent.supp_vehicule_suivant(self)
        self.vehicule_precedent = None
        self.propager_racine(self)
        
    def change_arbre(self, vehicule_precedent):
        """
            Se décroche de l'arbre actuel et se rattache à un autre sur un élément
                # vehicule_precedent : élément sur lequel on se rattache
                # @author : Marcus
        """
        if (vehicule_precedent.racine == self.racine):
            return
        if (self.vehicule_precedent is None):
            self.simulateur.del_listener(self)
        self.vehicule_precedent.supp_vehicule_suivant(self)
        self.set_vehicule_precedent(vehicule_precedent)
        vehicule_precedent.add_vehicule_suivant(self)
        self.propager_racine(vehicule_precedent.racine)

    def propager_racine(self, racine):
        """
            Met à jour sa racine et transmet l'information aux fils
                # racine : nouvelle racine
                # @author : Marcus
        """
        self.racine = racine
        if (len(self.vehicules_suivants) != 0):
            for vehicule_suivant in self.vehicules_suivants:
                vehicule_suivant.propager_racine(racine)

    def set_vehicule_precedent(self, vehicule):
        self.vehicule_precedent = vehicule

    def set_vehicules_suivants(self, vehicules):
        self.vehicules_suivants = vehicules

    def add_vehicule_suivant(self, vehicule):
        self.vehicules_suivants.append(vehicule)

    def supp_vehicule_suivant(self, vehicule):
        self.vehicules_suivants.remove(vehicule)

    def donner_arriere(self):
        return (self.coordonnees - self.direction * self.longueur)

        
    def mettre_coordonnees_a_jour(self, increment_temps, nb_ticks_sec, vitesse_obstacle, position_obstacle):
        #print("Coordonnees mises à jour")

        dx = self.vitesse.x * increment_temps / nb_ticks_sec
        dy = self.vitesse.y * increment_temps / nb_ticks_sec

        #print("Delta x : "+str(dx))
        #print("Delta y : "+str(dy))

        dv = self.acceleration * (increment_temps / nb_ticks_sec) * 100
        dvx = dv.x
        dvy = dv.y
            
        vitesse_max = self.voie.vitesse_max

        if self.intersection != None:
            Vehicule.vitesse_max = Intersection.Intersection.vitesse_max

        if vitesse_obstacle is None:
            vitesse_obstacle = self.direction * vitesse_max

        acceleration_libre = 1 - (float(abs(self.vitesse))/(abs(vitesse_max)))**4
        acceleration_approche = 0
        
        #print("Obstacle : "+str(position_obstacle))

        if position_obstacle is not None:
            acceleration_approche =  Vehicule.distance_minimale/100.0 # s_0
            acceleration_approche +=  abs(self.vitesse)/100.0 * Vehicule.temps_reaction # += v_aT 
            acceleration_approche += (abs(self.vitesse) / 100.0 * (((self.vitesse - vitesse_obstacle)/100.0)*self.direction))/(2 * sqrt(Vehicule.acceleration_max * Vehicule.deceleration_conf)) # += 
            acceleration_approche /= abs(position_obstacle - self.coordonnees)/100.0
            acceleration_approche **= 2
        #print("Acceleration approche : "+str(acceleration_approche))

        val_acceleration = Vehicule.acceleration_max * (acceleration_libre - acceleration_approche)
        
        self.acceleration.x = val_acceleration * self.direction.x
        self.acceleration.y = val_acceleration * self.direction.y
            
        projection = Coordonnees.Coordonnees.changer_repere(self.coordonnees, self.origine, self.repere_trajectoire_axe_x)
        coeff_tangeante = 2 * self.poly_a * projection.x + self.poly_b
        orientation = Coordonnees.Coordonnees(1, coeff_tangeante)
        orientation = orientation.normaliser()
        self.direction= orientation
           
        self.vitesse.x += dvx
        self.vitesse.y += dvy
        #~ print("avant Luc : " + str(self.vehicules_suivants[0].coordonnees))
        self.coordonnees = Coordonnees.Coordonnees(self.coordonnees.x + dx, self.coordonnees.y + dy)
        #~ print("après Luc : " + str(self.vehicules_suivants[0].coordonnees))

    def changer_trajectoire(self, destination, orientation_cible):
        #print ("Changement Trajectoire")
        #print (destination)
        #print (orientation_cible)
        #print ("Fin trace changement trajectoire")
        self.orientation_cible = copy.copy(orientation_cible)
        self.destination = copy.copy(destination)
        self.origine = copy.copy(self.coordonnees)
        self.orientation_origine = copy.copy(self.direction)
        self.repere_trajectoire_axe_x = self.destination - self.origine
        self.repere_trajectoire_axe_x = self.repere_trajectoire_axe_x.normaliser()
        self.repere_trajectoire_axe_y = Coordonnees.Coordonnees(-self.repere_trajectoire_axe_x.y, self.repere_trajectoire_axe_x.x)

        dest_nv_rep = Coordonnees.Coordonnees.changer_repere(self.destination, self.origine, self.repere_trajectoire_axe_x)

        orientation_nv_rep = Coordonnees.Coordonnees.changer_repere(self.orientation_cible, self.origine, self.repere_trajectoire_axe_x)
            
        ratio = (dest_nv_rep.y - orientation_nv_rep.y) / (dest_nv_rep.x - 2)

        self.poly_a = ratio / dest_nv_rep.x
        self.poly_b = orientation_nv_rep.y - 2 * ratio
        print("a : " + str(self.poly_a) + " b : " + str(self.poly_b))

    """
   def calculer_trajet_max(self, coordonnees_destination):
       distance_vecteur = coordonnees_destination.soustraction(self.coordonnees)
       distance_normee = distance_vecteur.norme()
       #distance_possible = min (self.calculerVitesse() , distance_normee)
       trajet = self.direction.mult(distance_possible)
       resultat = self.coordonnees.addition(trajet)
       return resultat

   def suit_vehicule_devant(self):
       marge = self.direction.mult(self.vehicule_precedent.longueur + self.distance_minimale) #longueur + distance minimale
       distance = self.vehicule_precedent.coordonnees.soustraction(marge)
       resultat = self.calculer_trajet_max(distance)
       self.coordonnees = resultat
       #on avance de ce que l'on peut

   def verifie_feu(self):
       return self.voie.est_passant(self.prochaine_direction)

   def avance_feu(self):
       resultat = self.calculer_trajet_max(self.voie.coordonnees_fin)
       distance_faite = abs(resultat - self.coordonnees)
       self.coordonnees = resultat
       return distance_faite

   def avance_change_voie(self):
       trajet = self.calculer_trajet_max(self.destination.soustraction(self.direction.mult(30)))
       self.coordonnees = self.coordonnees.addition(trajet)

   def avancer_intersection(self, distance_faite):
       trajet = self.calculer_trajet_max(self.destination)

       """
