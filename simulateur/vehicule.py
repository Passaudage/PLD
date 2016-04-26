import coordonnees

class vehicule:
    acceleration = coordonnees(0,0)
    vitesse = coordonnees(0,0)
    est_arrete = False

    def __init__(self, coordonnees, aggressivite, longueur, voie, prochaine_direction):
        self.coordonnees = coordonnees
        self.aggressivite = aggressivite
        self.longueur = longueur
        self.changeDirection(0,0)
        self.voie = voie
        self.prochaine_direction = prochaine_direction
        self.vehicule_precedent
        self.vehicule_suivant = []
    
    def changeDirection(self, x, y):
        self.direction = coordonnees(x, y)

    def avancerBoucle(pasTemporel):

        return False



    def calculerVitesse(self):
        return


    def notify(self):
        return

    def avancer(self, prochaine_voiture):
        return

    def set_vehicule_precedent(self, vehicule):
        self.vehicule_precedent = vehicule
        vehicule.set_vehicule_suivant(self)


    def set_vehicule_suivant(self, vehicule):
        self.vehicule_suivant.append(vehicule)

