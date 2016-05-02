import Intersection

class Apprentissage:

    def __init__(self, simulateur):
        self.simulateur = simulateur

        self.intersections = []
        self.reseaux_action = []
        self.agents = []
        self.experiments = []

        for listener in self.simulateur.listeners:
            if type(listener) is Intersection.Intersection:
                self.intersections.append(listener)

        if not self.intersections:
            raise Exception("Aucune intersection enregistrées au simulateur")

        self.nb_variables_trafic = len(self.intersections[0].recuperer_etat_trafic())

        for intersection in self.intersections:
            # Initialiser le réseau pour l'apprentissage
            reseaux_action.append( ActionValueNetwork(self.nb_variables_trafic,
                        len(intersection.combinaisons)) )

            # Classe d'apprentissage
            learner = NFQ()
            learner.explorer.epsilon = 0.4 # TODO : à tuner

            agents.append(LearningAgent(av_network, learner))
            env = EnvironnementUrbain(intersection, sim)
            task = SimulationIntersectionTask(env)
            experiments.append(Experiment(task, agent))

    def demarrer_apprentissage(self, duree):
        """
            nb_tours_simulateur : nombre d'incréments de temps
            entre chaque prise en compte de l'environnement

            nb_interactions : nombre de prise en compte de l'environnement
            avant chaque apprentissage (nombre d'élément dans un minibatch)
        """

        nb_tours_simulateur = 0
        nb_interactions = 0

        accumulateur = 0

        while accumulateur < duree:

            for i in range(nb_interactions):
                for experiment in experiments:
                    experiment.doInteractions(1)

                # faire avancer la simulation
                for s in range(nb_tours_simulateur):
                    self.simulateur.avance_temps()

            for agent in self.agents:
                agent.learn()

            accumulateur += self.simulateur.grain


            for i in range(nombre_interactions):
                experiment.doInteractions()








        

