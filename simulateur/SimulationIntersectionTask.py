from pybrain.rl.environments.task import Task

class SimulationIntersectionTask(Task):
    """ A task is associating a purpose with an environment. It decides how to evaluate the observations, potentially returning reinforcement rewards or fitness values.
    Furthermore it is a filter for what should be visible to the agent.
    Also, it can potentially act as a filter on how actions are transmitted to the environment. """

    def __init__(self, environnement):
        self.environnement = environnement
        self.derniere_recompense = 0

    def performAction(self, action):
        """
            Demande à l'environnement de répercuter un changement : changer
            la configuration courante des feux de l'intersection correspondante.
        """               
        self.environnement.performAction(action)
       
    def getObservation(self):
        """
            Récupère la description de l'environnement (état du trafic).
        """

        return self.environnement.getSensors()
   
    def getReward(self):
        """
            On a S0 : on veut évaluer cette configuration.
        """

        etat_trafic = self.getObservation()
        
        recompense = self.environnement.intersection.evaluer_situation()

        print("Récompense : " + str(recompense))

        # On récupère la dernière récompense
        # et on sauvegarde la nouvelle
        cur_recompense = self.derniere_recompense
        self.dernire_recompense = recompense
    
        return cur_recompense