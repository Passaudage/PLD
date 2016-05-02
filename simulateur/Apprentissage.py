from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import NFQ
from pybrain.rl.experiments import Experiment

import Intersection
import SimulationIntersectionTask
import EnvironnementUrbain

import threading

class Apprentissage:

    nb_tours_simulateur = 0
    nb_interactions = 4

    def __init__(self, simulateur):
        self.simulateur = simulateur

        self.intersections = []
        self.reseaux_action = []
        self.agents = []
        self.experiments = []
        self.terminated = False

        for listener in self.simulateur.listeners:
            if type(listener) is Intersection.Intersection:
                self.intersections.append(listener)

        if not self.intersections:
            raise Exception("Aucune intersection enregistrée au simulateur")

        self.nb_variables_trafic = len(self.intersections[0].recuperer_etat_trafic())

        for intersection in self.intersections:
            # Initialiser le réseau pour l'apprentissage
            av_network = ActionValueNetwork(self.nb_variables_trafic,
                        len(intersection.combinaisons))
            self.reseaux_action.append(av_network)

            # Classe d'apprentissage
            learner = NFQ()
            learner.explorer.epsilon = 0.4 # TODO : à tuner

            agent = LearningAgent(av_network, learner)
            self.agents.append(agent)

            env = EnvironnementUrbain.EnvironnementUrbain(intersection, self.simulateur)
            task = SimulationIntersectionTask.SimulationIntersectionTask(env)
            self.experiments.append(Experiment(task, agent))

        thread = threading.Thread(None, self.demarrer_apprentissage, kwargs = {'duree' : 1})

        thread.start()


    def demarrer_apprentissage(self, duree):
        """
            nb_tours_simulateur : nombre d'incréments de temps
            entre chaque prise en compte de l'environnement

            nb_interactions : nombre de prise en compte de l'environnement
            avant chaque apprentissage (nombre d'élément dans un minibatch)
        """

        duree *= self.simulateur.nombre_ticks_seconde

        accumulateur = 0

        while accumulateur < duree:

            for i in range(Apprentissage.nb_interactions):
                for experiment in self.experiments: # potentiellement multithreadable
                    experiment.doInteractions(1)

                # faire avancer la simulation
                for s in range(Apprentissage.nb_tours_simulateur):
                    self.simulateur.avance_temps()

                if self.terminated: # juste pour éviter de trop attendre
                    break

            for agent in self.agents: # potentiellement multithreadable
                agent.learn()

            accumulateur += self.simulateur.grain

            if self.terminated: # juste pour éviter de trop attendre
                break

        print("Fin apprentissage")

    def notifier_fin(self):
        self.terminated = True




        

