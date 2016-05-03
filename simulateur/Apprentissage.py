from pybrain.rl.learners.valuebased import ActionValueNetwork, ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import NFQ, Q
from pybrain.rl.experiments import Experiment

import Intersection
import SimulationIntersectionTask
import EnvironnementUrbain

import threading
import pickle

class Apprentissage:

    nb_second_increment_simulateur = 5 # en secondes
    nb_interactions = 4

    def __init__(self, simulateur):
        self.simulateur = simulateur

        self.intersections = []
        self.reseaux_action = {}
        self.agents = []
        self.experiments = []
        self.terminated = False
        self.apprentissage_termine = False
        self.apprentissage_en_cours = False

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
            self.reseaux_action[intersection] = av_network

            # Classe d'apprentissage
            learner = NFQ()
            learner.explorer.epsilon = 0.7 # TODO : à tuner

            agent = LearningAgent(av_network, learner)
            self.agents.append(agent)

            env = EnvironnementUrbain.EnvironnementUrbain(intersection, self.simulateur)
            task = SimulationIntersectionTask.SimulationIntersectionTask(env)
            self.experiments.append(Experiment(task, agent))

        self.derouler_simulateur_libre(60)

        thread = threading.Thread(None, self.demarrer_apprentissage,
                kwargs = {'duree' : 3600})

        thread.start()

    def derouler_simulateur_libre(self, duree):

        duree *= self.simulateur.nombre_ticks_seconde
        accumulateur = 0

        while accumulateur < duree:
            self.simulateur.avance_temps()
            accumulateur += self.simulateur.grain

    def demarrer_apprentissage(self, duree):
        """
            nb_tours_simulateur : nombre d'incréments de temps
            entre chaque prise en compte de l'environnement

            nb_interactions : nombre de prise en compte de l'environnement
            avant chaque apprentissage (nombre d'élément dans un minibatch)
        """
        self.apprentissage_en_cours = True
        duree *= self.simulateur.nombre_ticks_seconde

        nb_tours_simulateur = int((self.nb_second_increment_simulateur * self.simulateur.nombre_ticks_seconde) / self.simulateur.grain)

        accumulateur = 0

        while accumulateur < duree:

            for i in range(self.nb_interactions):
                for experiment in self.experiments: # potentiellement multithreadable
                    experiment.doInteractions(1)

                # faire avancer la simulation
                for s in range(nb_tours_simulateur):
                    self.simulateur.avance_temps()

                if self.terminated: # juste pour éviter de trop attendre
                    break

            for agent in self.agents: # potentiellement multithreadable
                print("learning")
                agent.learn()
                print(" ok...")

            accumulateur += self.simulateur.grain * nb_tours_simulateur * self.nb_interactions
            print("Temps passé simulation : " + str(accumulateur/self.simulateur.nombre_ticks_seconde))

            if self.terminated: # juste pour éviter de trop attendre
                break

        sauvegarder_modele()

        self.apprentissage_en_cours = False
        self.apprentissage_termine = True
        print("Fin apprentissage")

    def notifier_fin(self):
        self.terminated = True

    def sauvegarder_modele(nom_fichier = "reseau.pkl"):
        pickle.dump(self.reseaux_action, open(nom_fichier, 'wb'))

    def restaurer_modele(nom_fichier = "reseau.pkl"):
        pkl_file = open(nom_fichier, 'rb')

        reseaux_action = pickle.load(pkl_file)

        #for reseau in reseaux_action:
        #    print("reseau : " + str(reseau.getMaxAction(self.intersections[0].recuperer_etat_trafic())))

        pkl_file.close()

        return reseaux_action


        

