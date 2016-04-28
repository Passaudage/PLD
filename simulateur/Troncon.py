import Coordonnees
import Feu
import Voie
import Vehicule

class Troncon:
    const_largeur_voie = 350 #centimètres, largeur standard d'une voie en France

    def __init__(self, intersection_tete, intersection_queue, coordonnees_debut, coordonnees_fin, proba_dir_sens1, proba_dir_sens2):  #sens1 : gauche vers droite, bas vers haut
        self.intersection_tete = intersection_tete #en haut ou à droite
        self.intersection_queue = intersection_queue #en bas ou à gauche
        self.coordonnees_debut = coordonnees_debut
        self.coordonnees_fin = coordonnees_fin
        self.longueur = (self.coordonnees_fin-coordonnees_debut).__abs__()
        self.trajectoire = (self.coordonnees_fin-coordonnees_debut).normaliser()
        self.proba_dir_sens1 = proba_dir_sens1
        self.proba_dir_sens2 = proba_dir_sens2
        self.directions_sens1 = self.proba_dir_sens1.keys()
        self.directions_sens2 = self.proba_dir_sens2.keys()
        self.voies_sens1 = []
        self.voies_sens2 = []
        self.dir_voies_sens1 = {"G": [], "TD": [], "D": []}
        self.dir_voies_sens2 = {"G": [], "TD": [], "D": []}
        self.dir_feu_sens1 = {}
        self.dir_feu_sens2 = {}
        self.feux_sens1 = {}
        self.feux_sens2 = {}

        for direction in self.directions_sens1 :
            self.dir_feu_sens1[direction] = Feu.Feu(self.intersection_tete, 20)

        for direction in self.directions_sens2:
            self.dir_feu_sens2[direction] = Feu.Feu(self.intersection_queue, 20)

    def ajouter_feux(self, sens, direction, feu):
        if(sens==1):
            if(direction == 'D'):
                self.feux_sens1['D'] = feu
            elif(direction == 'G'):
                self.feux_sens1['G'] = feu
            elif(direction == 'TD'):
                self.feux_sens1['TD'] = feu
            else:
                raise Exception("Mauvaise destination.")

        elif(sens==2):
            if(direction == 'D'):
                self.feux_sens2['D'] = feu
            elif(direction == 'G'):
                self.feux_sens2['G'] = feu
            elif(direction == 'TD'):
                self.feux_sens2['TD'] = feu
            else:
                raise Exception("Mauvaise destination.")

    # on crée les voies de l'intérieur vers l'extérieur dans les deux sens, l'utilisateur fera donc attention aux directions qu'il passe en paramètre (gauche d'abord)
    def creer_voie(self, directions, sens, vitesse_max):
        coordonnees_debut = None
        coordonnees_fin = None
        if (sens == "sens1") :
            if (self.coordonnees_debut.x == self.coordonnees_fin.x) :
                coordonnees_debut = Coordonnees.Coordonnees(self.coordonnees_debut.x + ((len(self.voies_sens1)) + 0.5)*self.const_largeur_voie, self.coordonnees_debut.y )
                coordonnees_fin = Coordonnees.Coordonnees(self.coordonnees_debut.x + (len(self.voies_sens1) + 0.5)*self.const_largeur_voie, self.coordonnees_fin.y )
            if (self.coordonnees_debut.y == self.coordonnees_fin.y):
                coordonnees_debut = Coordonnees.Coordonnees(self.coordonnees_debut.x,self.coordonnees_debut.y - (len(self.voies_sens1) + 0.5)*self.const_largeur_voie)
                coordonnees_fin = Coordonnees.Coordonnees(self.coordonnees_fin.x ,self.coordonnees_fin.y - (len(self.voies_sens1) + 0.5)*self.const_largeur_voie)

            proba_dir = {}
            proba_sum = 0
            proba_entree = 0
            for direction in directions :
                proba_entree = proba_entree + self.proba_dir_sens1[direction]/(len(self.dir_voies_sens1[direction]) +1) #la nouvelle voie n'est pas encore dans la liste
                proba_dir[direction] = self.proba_dir_sens1.get(direction)
                proba_sum = proba_sum + self.proba_dir_sens1.get(direction)

            for direction in directions :
                proba_dir[direction] = proba_dir.get(direction)/proba_sum
                #self, troncon, coordonnees_debut, coordonnees_fin, directions, proba_entree, proba_dir, vitesse_max):
            v = Voie.Voie(self, coordonnees_debut, coordonnees_fin, directions, proba_entree, proba_dir, Vehicule.v_max)
            self.voies_sens1.append(v)
            for direction in directions:
                self.dir_voies_sens1[direction] = [self.dir_voies_sens1.get(direction)] + [v]

        if (sens == "sens2"):
            if (self.coordonnees_debut.x == self.coordonnees_fin.x):
                coordonnees_debut = Coordonnees.Coordonnees(self.coordonnees_debut.x - (len(self.voies_sens2) + 0.5)*self.const_largeur_voie, self.coordonnees_debut.y)
                coordonnees_fin = Coordonnees.Coordonnees(self.coordonnees_debut.x - (len(self.voies_sens2) + 0.5)*self.const_largeur_voie, self.coordonnees_fin.y)
            if (self.coordonnees_debut.y == self.coordonnees_fin.y):
                coordonnees_debut = Coordonnees.Coordonnees(self.coordonnees_debut.x, self.coordonnees_debut.y + (len(self.voies_sens2) + 0.5)*self.const_largeur_voie)
                coordonnees_fin = Coordonnees.Coordonnees(self.coordonnees_fin.x, self.coordonnees_fin.y + (len(self.voies_sens2) + 0.5)*self.const_largeur_voie)

            proba_dir = {}
            proba_sum = 0
            proba_entree = 0
            for direction in directions:
                proba_entree = proba_entree + self.proba_dir_sens2[direction]/(len(self.dir_voies_sens2[direction]) + 1)  # la nouvelle voie n'est pas encore dans la liste
                proba_dir[direction] = self.proba_dir_sens2.get(direction)
                proba_sum = proba_sum + self.proba_dir_sens2.get(direction)

            for direction in directions:
                proba_dir[direction] = proba_dir.get(direction)/proba_sum

            v = Voie.Voie(self, coordonnees_debut, coordonnees_fin, directions, Coordonnees.Coordonnees(0, 0)-self.trajectoire, proba_entree, proba_dir)
            self.voies_sens2.append(v)
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

    def get_feu(self, direction, sens):
        if(sens == "sens1") :
            return self.dir_feu_sens1[direction]
        if (sens == "sens2"):
            return self.dir_feu_sens2[direction]

    def get_intersection(self, voie):
        if(voie in self.voies_sens1):
            return self.intersection_tete
        else : return self.intersection_queue

    def largeur(self):
        return (len(self.voies_sens1) + len(self.voies_sens2))*self.const_largeur_voie

    """
    ainsi toujours poussé vers de nouveaux rivages
    dans la nuit éternelle emporté sans retour
    ne pourrons nous jamais sur l'océan des ages
    jetez l'ancre un seul jour ?
        AdL
    """
