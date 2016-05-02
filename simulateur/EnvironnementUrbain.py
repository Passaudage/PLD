from pybrain.rl.environments.environment import Environment

class EnvironnementUrbain(Environment):
    """
        Représente l'environnement dans lequel se passe l'apprentissage.
        Comme on raisonne à l'échelle locale, ça correspond à une intersection.
    """
    def __init__(self, intersection, simulateur) :
        # on lui passe l'intersection pour laquelle il doit optimiser le trafic
        self.intersection = intersection
        self.simulateur = simulateur

    def getSensors(self):
        """ 
            Etat actuel du trafic : retourne un tableau de nombres (mesures sur le trafic)
        """
        print("Récupération état du trafic")
        return self.intersection.recuperer_etat_trafic()

    def performAction(self, action):
        """
            Action décidée par le réseau de neurone.
            action : une des configurations valide de feux.
        """

        print("Action : " + str(action[0]))

        # on change les feux
        duree_validite = self.intersection.appliquer_config(action[0])

    def reset(self):
        """ Most environments will implement this optional method that allows for reinitialization.
        """
