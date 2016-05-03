from pybrain.rl.learners.valuebased import ActionValueNetwork, ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import NFQ, Q
from pybrain.rl.experiments import Experiment

import Intersection
import SimulationIntersectionTask
import EnvironnementUrbain

import threading
import pickle

import Vehicule

import main
import jacky
import DoubleCarrefour
import TripleCarrefour


def get_simulateur():

    sim = jacky.charger_simulateur()
    #sim = DoubleCarrefour.charger_simulateur()
    #~ sim = TripleCarrefour.charger_simulateur()

    return sim

class ThreadLearning (threading.Thread):
    def __init__(self, agent):
        threading.Thread.__init__(self)
        self.agent = agent

    def run(self):
        self.agent.learn()


class Apprentissage:

    nb_interactions = 3 # nombre d'exemples dans un minibatch

    def __init__(self, simulateur, increment_simulateur_apprentissage, duree):
        self.simulateur = simulateur

        self.intersections = []
        self.reseaux_action = {}
        self.agents = []
        self.experiments = []
        self.tasks = {}
        self.terminated = False
        self.apprentissage_termine = False
        self.apprentissage_en_cours = False
        self.nb_seconde_increment_simulateur = increment_simulateur_apprentissage

        for listener in self.simulateur.listeners:
            if type(listener) is Intersection.Intersection:
                self.intersections.append(listener)

        if not self.intersections:
            raise Exception("Aucune intersection enregistrée au simulateur")

        self.nb_variables_trafic = len(self.intersections[0].recuperer_etat_trafic())

        self.nb_etats_entree = 531441

        for intersection in self.intersections:
            # Initialiser le réseau pour l'apprentissage
            #av_network = ActionValueNetwork(self.nb_variables_trafic,
            #            len(intersection.combinaisons))

            av_network = ActionValueTable(self.nb_etats_entree,
                        len(intersection.combinaisons))
            av_network.initialize()

            self.reseaux_action[str(intersection.coordonnees)] = av_network

            # Classe d'apprentissage
            #learner = NFQ()
            #learner.explorer.epsilon = 2 # TODO : à tuner

            #### Q-learning ####
            alpha = 0.6 # learning rate
            gamma = 0.5 # proche de zéro : optimisation à court terme

            learner = Q(alpha, gamma)
            learner.explorer.epsilon = 0.4
            ####################

            agent = LearningAgent(av_network, learner)
            self.agents.append(agent)

            env = EnvironnementUrbain.EnvironnementUrbain(intersection, self.simulateur)
            
            task = SimulationIntersectionTask.SimulationIntersectionTask(env)
            self.tasks[str(intersection.coordonnees)] = task
            self.experiments.append(Experiment(task, agent))

        self.duree_initiale = 10 # en secondes

        thread = threading.Thread(None, self.demarrer_apprentissage,
                kwargs = {'duree' : duree})

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

        nb_tours_simulateur = int((self.nb_seconde_increment_simulateur * self.simulateur.nombre_ticks_seconde) / self.simulateur.grain)
        nb_minibatch = 12

        accumulateur = 0

        compteur_minibatch = 0

        while accumulateur < duree:

            if compteur_minibatch >= nb_minibatch:

                # reset du simulateur
                print("Reset du simulateur")
                Vehicule.Vehicule.liste_voitures = []
                self.simulateur = get_simulateur()
                self.derouler_simulateur_libre(self.duree_initiale)

                compteur_minibatch = 0

                intersections = []

                for listener in self.simulateur.listeners:
                    if type(listener) is Intersection.Intersection:
                        intersections.append(listener)

                for intersection in intersections:
                    self.tasks[str(intersection.coordonnees)].changer_intersection(intersection)

            for i in range(self.nb_interactions):
                for experiment in self.experiments: # potentiellement multithreadable
                    experiment.doInteractions(1)

                # faire avancer la simulation
                for s in range(nb_tours_simulateur):
                    self.simulateur.avance_temps()

                if self.terminated: # juste pour éviter de trop attendre
                    break

            threads = []
            for agent in self.agents: # potentiellement multithreadable
                print("learning")
                thread = ThreadLearning(agent)
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
            print(" ok...")

            
            print("Temps passé simulation : " + str(accumulateur/self.simulateur.nombre_ticks_seconde))

            if self.terminated: # juste pour éviter de trop attendre
                break

            compteur_minibatch += 1

            if compteur_minibatch == nb_minibatch:
                accumulateur += self.simulateur.grain * nb_tours_simulateur * self.nb_interactions

        self.sauvegarder_modele()

        self.apprentissage_en_cours = False
        self.apprentissage_termine = True
        print("Fin apprentissage")

    def notifier_fin(self):
        self.terminated = True

    def sauvegarder_modele(self, nom_fichier = "reseau.pkl"):
        pickle.dump(self.reseaux_action, open(nom_fichier, 'wb'))

def restaurer_modele(nom_fichier = "reseau.pkl"):
    pkl_file = open(nom_fichier, 'rb')

    reseaux_action = pickle.load(pkl_file)

    pkl_file.close()

    return reseaux_action


        

