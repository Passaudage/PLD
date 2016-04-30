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
        self.longueur = abs((self.coordonnees_fin-coordonnees_debut))
        self.trajectoire = (self.coordonnees_fin-coordonnees_debut).normaliser()
        self.directions_sens1 = directions_sens_1
        self.directions_sens2 = directions_sens_2
        self.voies_sens1 = []
        self.voies_sens2 = []
        self.dir_voies_sens1 = {"G": [], "TD": [], "D": []}
        self.dir_voies_sens2 = {"G": [], "TD": [], "D": []}
        self.feux_sens1 = {}
        self.feux_sens2 = {}

        tete_presente = queue_presente = True 
        if(self.intersection_queue==None):
            queue_presente = False
        elif(self.intersection_tete==None):
            tete_presente = False

        if(coordonnees_debut.x == coordonnees_fin.x):
            if tete_presente: self.intersection_tete.branche_troncon(self, "B") 
            if queue_presente: self.intersection_queue.branche_troncon(self, "H")
        elif(coordonnees_fin.y == coordonnees_debut.y):
            if tete_presente: self.intersection_tete.branche_troncon(self, "G")
            if queue_presente: self.intersection_queue.branche_troncon(self, "D")
        
    def ajouter_generateur(self, sens, generateur):
        if(sens=="sens2"):
            self.feux_sens1['D'] = generateur
            self.feux_sens1['G'] = generateur
            self.feux_sens1['TD'] = generateur
            generateur.ajoute_voie_entrante(self.voies_sens1)
            generateur.ajoute_voie_sortante(self.voies_sens2)
        else:
            self.feux_sens2['D'] = generateur
            self.feux_sens2['G'] = generateur
            self.feux_sens2['TD'] = generateur 
            generateur.ajoute_voie_entrante(self.voies_sens2)
            generateur.ajoute_voie_sortante(self.voies_sens1)
                   
    def ajouter_feux(self, sens, direction, feu):
        print(str(sens))
        if(sens=="sens1"):
            self.feux_sens1[direction] = feu
        else:
            self.feux_sens2[direction] = feu

    def afficher_feux(self):
        for direction in self.feux_sens1.keys():
            print("feu sens 1 dans la direction suivante : " + direction + " est " + str(self.feux_sens1.get(direction).est_passant()))

        for direction in self.feux_sens2.keys():
            print("feu sens 2 dans la direction suivante : " + direction + " est " + str(
                self.feux_sens2.get(direction).est_passant()))


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
                coordonnees_debut = Coordonnees.Coordonnees(self.coordonnees_fin.x - (len(self.voies_sens2) + 0.5)*self.const_largeur_voie, self.coordonnees_fin.y)
                coordonnees_fin = Coordonnees.Coordonnees(self.coordonnees_debut.x - (len(self.voies_sens2) + 0.5)*self.const_largeur_voie, self.coordonnees_debut.y)
            if (self.coordonnees_debut.y == self.coordonnees_fin.y):
                coordonnees_debut = Coordonnees.Coordonnees(self.coordonnees_fin.x, self.coordonnees_fin.y + (len(self.voies_sens2) + 0.5)*self.const_largeur_voie)
                coordonnees_fin = Coordonnees.Coordonnees(self.coordonnees_debut.x, self.coordonnees_debut.y + (len(self.voies_sens2) + 0.5)*self.const_largeur_voie)

            v = Voie.Voie(self, coordonnees_debut, coordonnees_fin, directions, Vehicule.Vehicule.v_max, sens)
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

    def est_passant(self, direction, sens):
        #~ print("sens :"+str(sens))
        #~ print("direction : "+str(direction))
        if(sens == "sens1") :
            #~ print(self.feux_sens1)
            return self.feux_sens1[direction].est_passant()
        if (sens == "sens2"):
            #~ print(self.feux_sens2)
            return self.feux_sens2[direction].est_passant()

    def get_intersection(self, voie):
        if(voie in self.voies_sens1):
            return self.intersection_tete
        else : return self.intersection_queue

    def get_proba_situation_voie(self, voie, directions):
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
