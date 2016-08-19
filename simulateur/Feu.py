from enum import Enum

class Couleur(Enum):
    """
        Enumération utilisée pour la couleur des feux
            # @author : Bonfante
    """
    rouge = 0
    vert = 1

class Feu():
    """
        Modélise un feu de signalisation.
            # intersection : Intersection sur laquelle agit le feu
            # couleur_direction : La couleur initiale du feu
            # @author : Bonfante
    """

    def __init__(self, intersection, sens):
        
        # Intersection où se trouve le feu
        self.intersection = intersection

        # Couleur actuel de l'axe passé en parametre
        self.vient_juste_de_passer_au_rouge = False
        if(sens == 0):
            self.passant = False
        else:
            self.passant = False
            self.vient_juste_de_passer_au_rouge = True
        
        print ("FEU : " + str(self.passant))

        self.timestampLastChange = 0

    def change_couleur(self, timestamp):

        """
            Change la couleur du feu

        """
        self.passant = not(self.passant)
        self.timestampLastChange = timestamp

    def est_passant(self):
        return self.passant

    def ticksRouge(self, timestamp):
        if self.passant:
            return 0
        return timestamp - self.timestampLastChange
