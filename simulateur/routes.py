import math

import coordonnees
import feu
import vehicule


class voie:
    def __init__(self, troncon, coordonnees_debut, coordonnees_fin, directions, trajectoire):
        self.intersectionsAccessibles = []
        self.troncon = troncon
        self.coordonnees_debut = coordonnees_debut
        self.coordonnees_fin = coordonnees_fin
        self.vehicules = []
        self.trajectoire = trajectoire
        self.directions = directions
        self.feux = feu;


    def creer_vehicule(self, discourtois, longueur):
        prochaine_direction = "droite"
        clio = vehicule(50, coordonnees(0,0), discourtois, longueur, self, prochaine_direction, self.trajectoire, None)
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
        self.vehicules.delete(vehicule)

    def dernier_vehicule(self):
        return self.vehicules(-1)

    def setTroncon(self, troncon):
        self.troncon = troncon

    def precedent(self, vehicule):
        if(self.vehicules.index(vehicule)==0):
            return None
        else:
            return self.vehicules.index(vehicule)-1

    def est_passant(self, direction):
        return self.troncon.getFeu(direction).est_passant()


class troncon:
    const_largeur_voie = 350 #centimètres
    def __init__(self, tete, queue, coordonnees_debut, coordonnees_fin, proba_dir_sens1, proba_dir_sens2):  #sens1 : gauche vers droite, bas vers haut
        self.tete = tete #en haut ou à droite
        self.queue = queue #en bas ou à gauche
        self.coordonees_debut = coordonnees_debut
        self.coordonees_fin = coordonnees_fin
        self.longueur = math.sqrt((self.coordonnees_fin.x-self.coordonnees_debut.x)**2 + (self.coordonnees_fin.y-self.coordonnees_debut.y)**2)
        self.trajectoire = coordonnees((self.coordonnees_fin.x-self.coordonnees_debut.x)/self.longueur, (self.coordonnees_fin.y-self.coordonnees_debut.y)/self.longueur)
        self.proba_dir_sens1 = proba_dir_sens1
        self.proba_dir_sens2 = proba_dir_sens2
        self.directions_sens1 = self.proba_dir_sens1.keys()
        self.directions_sens2 = self.proba_dir_sens2.keys()
        self.voies_sens1 = []
        self.voies_sens2 = []
        self.dir_voies = {}
        self.dir_feu = {}

        for direction in self.directions :
            self.dir_feu[direction] = feu(self.tete)

    def creer_voie(self, directions, sens):  #on crée les voies de l'intérieur vers l'extérieur dans les deux sens, l'utilisateur fera donc attention aux directions qu'il passe en paramètre (gauche d'abord)
        if( sens == "sens1") :
            if(self.coordonnees_debut.x == self.coordonnees_fin.x):
                coordonnees_debut = coordonnees(self.coordonees_debut.x + (len(self.voies_sens1) + 0,5)*self.const_largeur_voie, self.coordonnees_debut.y )
                coordonnees_fin = coordonnees(self.coordonees_debut.x + (len(self.voies_sens1) + 0,5)*self.const_largeur_voie, self.coordonnees_fin.y )
            if (self.coordonnees_debut.y == self.coordonnees_fin.y):
                coordonnees_debut = coordonnees(self.coordonees_debut.x,self.coordonnees_debut.y + (len(self.voies_sens1) + 0, 5) * self.const_largeur_voie)
                coordonnees_fin = coordonnees(self.coordonees_fin.x ,self.coordonnees_fin.y + (len(self.voies_sens1) + 0, 5) * self.const_largeur_voie)
            self.voies.append(voie(self, coordonnees_debut, coordonnees_fin, directions, self.trajectoire))

        if (sens == "sens2"):
            if (self.coordonnees_debut.x == self.coordonnees_fin.x):
                coordonnees_debut = coordonnees(self.coordonees_debut.x - (len(self.voies_sens1) + 0, 5) * self.const_largeur_voie, self.coordonnees_debut.y)
                coordonnees_fin = coordonnees(self.coordonees_debut.x - (len(self.voies_sens1) + 0, 5) * self.const_largeur_voie, self.coordonnees_fin.y)
            if (self.coordonnees_debut.y == self.coordonnees_fin.y):
                coordonnees_debut = coordonnees(self.coordonees_debut.x, self.coordonnees_debut.y - (len(self.voies_sens1) + 0, 5) * self.const_largeur_voie)
                coordonnees_fin = coordonnees(self.coordonees_fin.x, self.coordonnees_fin.y - (len(self.voies_sens1) + 0, 5) * self.const_largeur_voie)
            self.voies.append(voie(self, coordonnees_debut, coordonnees_fin, directions, self.trajectoire))



    #trouver voie avec bonne direction
    def trouver_voie_direction(self, direction):
        voies_possibles = []
        for voie in self.voies:
            if(voie.direction_possible(direction)):
                voies_possibles.append(voie)
        return voies_possibles

    def getFeu(self, direction):
        if(direction in self.dir_feu.keys()):
            return self.dir_feu.get(direction)
        else:
            self.dir_feu[direction] = feu(self.tete)
            return self.dir_feu.get(direction)


    """
    ainsi toujours poussé vers de nouveaux rivages
    dans la nuit éternelle emporté sans retour
    ne pourrons nous jamais sur l'océan des ages
    jetez l'ancre un seul jour ?
        AdL
    """
