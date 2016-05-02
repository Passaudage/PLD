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

    def notifie_temps(self, temps, simulation_manager):
        """
            Methode appelée lorsque le simulateur augmente le temps
        """
        pass
        #~ self.change_couleur(simulation_manager.temps)

    def change_couleur(self):

        """
                    Change la couleur du feu

        """
        if(not self.passant and self.vient_juste_de_passer_au_rouge):
            self.vient_juste_de_passer_au_rouge = False
        else:
            self.passant = not(self.passant)

    def est_passant(self):
        return self.passant

