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

    def __init__(self, intersection):
        
        # Intersection où se trouve le feu
        self.intersection = intersection

        # Couleur actuel de l'axe passé en parametre
        self.passant = True
        
        # Temps Vert 
        self.temps_vert = 100000
        
        # Temps cycle
        self.temps_cycle = 200000
        
        print ("FEU : " + str(self.passant))

    def notifie_temps(self, temps, simulation_manager):
        """
            Methode appelée lorsque le simulateur augmente le temps
        """
        pass
        print("ZOB : "+str(simulation_manager.temps) + " "+str(self)+ " "+str(self.passant))
        self.change_couleur(simulation_manager.temps)

    def change_couleur(self, temps):
        """
                    Change la couleur du feu

        """
        if(temps%self.temps_cycle <= self.temps_vert):
            self.passant = True
        else:
            self.passant = False
      
        #~ self.passant = not(self.passant)

    def est_passant(self):
        return self.passant

