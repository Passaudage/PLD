import Coordonnees
import Feu
import Voie

class Troncon:
    const_largeur_voie = 350 #centimètres, largeur standard d'une voie en France
    def __init__(self, tete, queue, coordonnees_debut, coordonnees_fin, proba_dir_sens1, proba_dir_sens2):  #sens1 : gauche vers droite, bas vers haut
        self.tete = tete #en haut ou à droite
        self.queue = queue #en bas ou à gauche
        self.coordonnees_debut = coordonnees_debut
        self.coordonnees_fin = coordonnees_fin
        self.longueur = self.coordonnees_debut.norme(coordonnees_fin)
        self.trajectoire = Coordonnees.Coordonnees((self.coordonnees_fin.x-self.coordonnees_debut.x)/self.longueur, (self.coordonnees_fin.y-self.coordonnees_debut.y)/self.longueur)
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
            self.dir_feu[direction] = Feu.Feu(self.tete)

    def creer_voie(self, directions, sens):  #on crée les voies de l'intérieur vers l'extérieur dans les deux sens, l'utilisateur fera donc attention aux directions qu'il passe en paramètre (gauche d'abord)
        coordonnees_debut = None
        coordonnees_fin = None
        if( sens == "sens1") :
            if(self.coordonnees_debut.x == self.coordonnees_fin.x):
                coordonnees_debut = Coordonnees.Coordonnees(self.coordonnees_debut.x + (len(self.voies_sens1) + 0,5)*self.const_largeur_voie, self.coordonnees_debut.y )
                coordonnees_fin = Coordonnees.Coordonnees(self.coordonnees_debut.x + (len(self.voies_sens1) + 0,5)*self.const_largeur_voie, self.coordonnees_fin.y )
            if (self.coordonnees_debut.y == self.coordonnees_fin.y):
                coordonnees_debut = Coordonnees.Coordonnees(self.coordonnees_debut.x,self.coordonnees_debut.y - (len(self.voies_sens1) + 0, 5)*self.const_largeur_voie)
                coordonnees_fin = Coordonnees.Coordonnees(self.coordonnees_fin.x ,self.coordonnees_fin.y - (len(self.voies_sens1) + 0, 5)*self.const_largeur_voie)

            proba_dir = {}
            proba_sum = 0
            proba_entree = 0
            for direction in directions :
                proba_entree = proba_entree + self.proba_dir_sens1[direction]/(len(self.dir_voies_sens1[direction]) +1) #la nouvelle voie n'est pas encore dans la liste
                proba_dir[direction] = self.proba_dir_sens1.get[direction]
                proba_sum = proba_sum + self.proba_dir_sens1.get[direction]

            for direction in directions :
                proba_dir[direction] = proba_dir.get(direction)/proba_sum

            v = Voie.Voie(self, coordonnees_debut, coordonnees_fin, directions, self.trajectoire, proba_entree, proba_dir)

            for direction in directions:
                self.dir_voies_sens1[direction] = [self.dir_voies_sens1.get(direction)] + [v]

        if (sens == "sens2"):
            if (self.coordonnees_debut.x == self.coordonnees_fin.x):
                coordonnees_debut = Coordonnees.Coordonnees(self.coordonnees_debut.x - (len(self.voies_sens2) + 0, 5)*self.const_largeur_voie, self.coordonnees_debut.y)
                coordonnees_fin = Coordonnees.Coordonnees(self.coordonnees_debut.x - (len(self.voies_sens2) + 0, 5)*self.const_largeur_voie, self.coordonnees_fin.y)
            if (self.coordonnees_debut.y == self.coordonnees_fin.y):
                coordonnees_debut = Coordonnees.Coordonnees(self.coordonnees_debut.x, self.coordonnees_debut.y + (len(self.voies_sens2) + 0, 5)*self.const_largeur_voie)
                coordonnees_fin = Coordonnees.Coordonnees(self.coordonnees_fin.x, self.coordonnees_fin.y + (len(self.voies_sens2) + 0, 5)*self.const_largeur_voie)

            proba_dir = {}
            proba_sum = 0
            proba_entree = 0
            for direction in directions:
                proba_entree = proba_entree + self.proba_dir_sens2[direction]/(len(self.dir_voies_sens2[direction]) + 1)  # la nouvelle voie n'est pas encore dans la liste
                proba_dir[direction] = self.proba_dir_sens2.get[direction]
                proba_sum = proba_sum + self.proba_dir_sens2.get[direction]

            for direction in directions:
                proba_dir[direction] = proba_dir.get(direction)/proba_sum

            v = Voie.Voie(self, coordonnees_debut, coordonnees_fin, directions, self.trajectoire, proba_entree, proba_dir)
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
            self.dir_feu[direction] = Feu.Feu(self.tete)
            return self.dir_feu.get(direction)


    """
    ainsi toujours poussé vers de nouveaux rivages
    dans la nuit éternelle emporté sans retour
    ne pourrons nous jamais sur l'océan des ages
    jetez l'ancre un seul jour ?
        AdL
    """
