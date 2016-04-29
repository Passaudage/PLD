import Coordonnees
import Feu
import Voie
import Vehicule

class Troncon:
    const_largeur_voie = 350 # centimètres

    def __init__(self, intersection_tete, intersection_queue, coordonnees_debut, coordonnees_fin, directions_sens_1, directions_sens_2):  #sens1 : gauche vers droite, bas vers haut
        self.intersection_tete = intersection_tete #en haut ou à droite
        self.intersection_queue = intersection_queue #en bas ou à gauche
        self.coordonnees_debut = coordonnees_debut
        self.coordonnees_fin = coordonnees_fin
        self.longueur = (self.coordonnees_fin-coordonnees_debut).__abs__()
        self.trajectoire = (self.coordonnees_fin-coordonnees_debut).normaliser()
        self.directions_sens1 = directions_sens_1
        self.directions_sens2 = directions_sens_2
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
        
        coordonnees_queue = self.intersection_queue.coordonnees_debut
        coordonnees_tete = self.intersection_tete.coordonnees_debut
        if(coordonnees_queue.x == coordonnees_tete.x):
			self.intersection_tete.branche_troncon(self, B)
			self.intersection_queue.branche_troncon(self, H)
		elif(coordonnees_queue.y == coordonnees_tete.y):
			self.intersection_tete.branche_troncon(self, G)
			self.intersection_queue.branche_troncon(self, D)
			
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

            v = Voie.Voie(self, coordonnees_debut, coordonnees_fin, directions, Vehicule.Vehicule.v_max, sens)
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

            v = Voie.Voie(self, coordonnees_debut, coordonnees_fin, directions, Coordonnees.Coordonnees(0, 0)-self.trajectoire, sens)
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

    def get_proba_situation_voie(self, voie, directions):
        dico_voies = {}
        intersection = None
        if (voie.sens == "sens1"):
            dico_voies = self.dir_voies_sens1
            intersection = self.intersection_tete
        else: 
            dico_voies = self.dir_voies_sens2
            intersection = self.intersection_queue
        proba = 0
        for direction in directions:
            proba += intersection.get_proba(self, direction)/len(dico_voies.get(direction))
        return proba

    def largeur(self):
        return (len(self.voies_sens1) + len(self.voies_sens2))*self.const_largeur_voie

    """
    ainsi toujours poussé vers de nouveaux rivages
    dans la nuit éternelle emporté sans retour
    ne pourrons nous jamais sur l'océan des ages
    jetez l'ancre un seul jour ?
        AdL
    """
