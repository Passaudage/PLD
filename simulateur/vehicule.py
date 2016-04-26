import coordonnees

class vehicule:
    acceleration = coordonnees(0,0)
    vitesse = coordonnees(0,0)
    est_arrete = False

    def __init__(self, max_acceleration, coordonnees, aggressivite, longueur, voie, prochaine_direction, racine):
        self.coordonnees = coordonnees
        self.max_acceleration = max_acceleration
        self.aggressivite = aggressivite
        self.longueur = longueur
        self.voie = voie
        self.prochaine_direction = prochaine_direction
        self.vehicule_precedent
        self.vehicule_suivant = []
        self.racine = racine
        self.direction
        self.voie_actuelle
        self.intersection_actuelle

    
    def changeDirection(self, x, y):
        self.direction = coordonnees(x, y)

    def avancerBoucle(pasTemporel):

        return False

    def calculerVitesse(self):

        return


    def notifie_temps(self):
        return

    def avance_vehicule(self, vehicule_suivant):
        #fait avancer le vehicule
        return

    def greffe_arbre(self, vehicule_precedent):
        self.set_vehicule_precedent(vehicule_precedent)
        vehicule_precedent.set_vehicule_suivant(self)

    def set_vehicule_precedent(self, vehicule):
        self.vehicule_precedent = vehicule


    def set_vehicule_suivant(self, vehicule):
        self.vehicule_suivant.append(vehicule)

    def propager_racine(self):

    def est_la_bonne_voie(self):
        #suis je sur la bonne direction ?
