import coordonnees

class vehicule:
    acceleration = coordonnees(0,0)
    vitesse = coordonnees(0,0)
    def __init__(self, coordonnees, aggressivite, longueur):
        self.coordonnees = coordonnees
        self.aggressivite = aggressivite
        self.longueur = longueur
        self.changeDirection(0,0)
    
    def changeDirection(self, x, y):
        self.direction = coordonnees(x, y)

    def avancerBoucle(pasTemporel):
        return False

