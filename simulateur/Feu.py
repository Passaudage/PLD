"""
    Celui qui n'a jamais eu de poule, l'abbreuve à la rivière.
"""

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

    def __init__(self, intersection, couleur_direction = Couleur.vert):
        # Intersection où se trouve le feu
        self.intersection = intersection

        # Couleur actuel de l'axe passé en parametre
        self.couleur_direction = couleur_direction

    def notifie_temps(self, temps, simulation_manager):
        """
            Methode appelée lorsque le simulateur augmente le temps
        """
        self.change_couleur()

    def change_couleur(self):
        """
            Change la couleur du feu
        """
        self.couleur_direction = 1-self.couleur_direction
		

    def est_passant(self):
        return self.couleur_direction == Couleur.vert

