import math

import coordonnees
import feu
import vehicule


class voie:
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
        clio = vehicule.vehicule(50, coordonnees.coordonnees(0,0), discourtois, longueur, self, prochaine_direction, self.trajectoire, None)
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


class troncon:
    const_largeur_voie = 350 #centimètres, largeur standard d'une voie en France
    def __init__(self, tete, queue, coordonnees_debut, coordonnees_fin, proba_dir_sens1, proba_dir_sens2):  #sens1 : gauche vers droite, bas vers haut
        self.tete = tete #en haut ou à droite
        self.queue = queue #en bas ou à gauche
        self.coordonnees_debut = coordonnees_debut
        self.coordonnees_fin = coordonnees_fin
        self.longueur = self.coordonnees_debut.norme(coordonnees_fin)
        self.trajectoire = coordonnees.coordonnees((self.coordonnees_fin.x-self.coordonnees_debut.x)/self.longueur, (self.coordonnees_fin.y-self.coordonnees_debut.y)/self.longueur)
        self.proba_dir_sens1 = proba_dir_sens1
        self.proba_dir_sens2 = proba_dir_sens2
        self.directions_sens1 = self.proba_dir_sens1.keys()
        self.directions_sens2 = self.proba_dir_sens2.keys()
        self.voies_sens1 = []
        self.voies_sens2 = []
        self.dir_voies_sens1 = {}
        self.dir_voies_sens2 = {}
        self.dir_feu = {}

        for direction in self.directions_sens1 :
            self.dir_feu[direction] = feu.feu(self.tete)

    def creer_voie(self, directions, sens):  #on crée les voies de l'intérieur vers l'extérieur dans les deux sens, l'utilisateur fera donc attention aux directions qu'il passe en paramètre (gauche d'abord)
        coordonnees_debut = None
        coordonnees_fin = None
        if( sens == "sens1") :
            if(self.coordonnees_debut.x == self.coordonnees_fin.x):
                coordonnees_debut = coordonnees.coordonnees(self.coordonnees_debut.x + (len(self.voies_sens1) + 0,5)*self.const_largeur_voie, self.coordonnees_debut.y )
                coordonnees_fin = coordonnees.coordonnees(self.coordonnees_debut.x + (len(self.voies_sens1) + 0,5)*self.const_largeur_voie, self.coordonnees_fin.y )
            if (self.coordonnees_debut.y == self.coordonnees_fin.y):
                coordonnees_debut = coordonnees.coordonnees(self.coordonnees_debut.x,self.coordonnees_debut.y - (len(self.voies_sens1) + 0, 5)*self.const_largeur_voie)
                coordonnees_fin = coordonnees.coordonnees(self.coordonnees_fin.x ,self.coordonnees_fin.y - (len(self.voies_sens1) + 0, 5)*self.const_largeur_voie)

            proba_dir = {}
            proba_sum = 0
            proba_entree = 0
            for direction in directions :
                proba_entree = proba_entree + self.proba_dir_sens1[direction]/(len(self.dir_voies_sens1[direction]) +1) #la nouvelle voie n'est pas encore dans la liste
                proba_dir[direction] = self.proba_dir_sens1.get[direction]
                proba_sum = proba_sum + self.proba_dir_sens1.get[direction]

            for direction in directions :
                proba_dir[direction] = proba_dir.get(direction)/proba_sum

            v = voie(self, coordonnees_debut, coordonnees_fin, directions, self.trajectoire, proba_entree, proba_dir)

            for direction in directions:
                self.dir_voies_sens1[direction] = [self.dir_voies_sens1.get(direction)] + [v]

        if (sens == "sens2"):
            if (self.coordonnees_debut.x == self.coordonnees_fin.x):
                coordonnees_debut = coordonnees.coordonnees(self.coordonnees_debut.x - (len(self.voies_sens2) + 0, 5)*self.const_largeur_voie, self.coordonnees_debut.y)
                coordonnees_fin = coordonnees.coordonnees(self.coordonnees_debut.x - (len(self.voies_sens2) + 0, 5)*self.const_largeur_voie, self.coordonnees_fin.y)
            if (self.coordonnees_debut.y == self.coordonnees_fin.y):
                coordonnees_debut = coordonnees.coordonnees(self.coordonnees_debut.x, self.coordonnees_debut.y + (len(self.voies_sens2) + 0, 5)*self.const_largeur_voie)
                coordonnees_fin = coordonnees.coordonnees(self.coordonnees_fin.x, self.coordonnees_fin.y + (len(self.voies_sens2) + 0, 5)*self.const_largeur_voie)
            self.voies_sens2.append(voie(self, coordonnees_debut, coordonnees_fin, directions, self.trajectoire))

            proba_dir = {}
            proba_sum = 0
            proba_entree = 0
            for direction in directions:
                proba_entree = proba_entree + self.proba_dir_sens2[direction]/(len(self.dir_voies_sens2[direction]) + 1)  # la nouvelle voie n'est pas encore dans la liste
                proba_dir[direction] = self.proba_dir_sens2.get[direction]
                proba_sum = proba_sum + self.proba_dir_sens2.get[direction]

            for direction in directions:
                proba_dir[direction] = proba_dir.get(direction)/proba_sum

            v = voie(self, coordonnees_debut, coordonnees_fin, directions, self.trajectoire, proba_entree, proba_dir)
            for direction in directions:
                self.dir_voies_sens2[direction] = [self.dir_voies_sens2.get(direction)] + [v]

    # end creer voie

    #trouver voie avec bonne direction
    def trouver_voie_direction(self, direction, sens):
        voies_possibles = []
        if(sens == "sens1") :
            for voie in self.voies_sens1:
                if(voie.direction_possible(direction)):
                    voies_possibles.append(voie)

        if(sens == "sens2") :
            for voie in self.voies_sens2:
                if(voie.direction_possible(direction)):
                    voies_possibles.append(voie)

        return voies_possibles

    def getFeu(self, direction):
        if(direction in self.dir_feu.keys()):
            return self.dir_feu.get(direction)
        else:
            self.dir_feu[direction] = feu.feu(self.tete)
            return self.dir_feu.get(direction)


    """
    ainsi toujours poussé vers de nouveaux rivages
    dans la nuit éternelle emporté sans retour
    ne pourrons nous jamais sur l'océan des ages
    jetez l'ancre un seul jour ?
        AdL
    """
