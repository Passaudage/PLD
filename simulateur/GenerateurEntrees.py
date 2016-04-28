from SimulationManager import *
from math import *
from random import *
import Vehicule
import numpy

def proba_poisson(k, freq, temps_obs):
        #Calcul du lambda correspondant
        l = freq * temps_obs
        p = e ** (-l)
        for i in range(0, k):
            p *= l/k
            k = k-1
        return p

def var_poisson(freq, temps_obs):
    proba_cumulee = random()
    k = 0
    proba_cumul_iter = proba_poisson(0, freq, temps_obs)
    while proba_cumul_iter < proba_cumulee:
        k += 1
        proba_cumul_iter += proba_poisson(k, freq, temps_obs)

    return k


class GenerateurEntrees:
    # Contrat : les heures_freqs : liste triées par heures croissantes
    # Les frequences sont en nombre de voitures par minutes
    duree_journee = 3600*24*SimulationManager.nombre_ticks_seconde
    def __init__(self, heures_freqs):
        self._attente = []
        self._heures_freqs = heures_freqs
        self._timestamp_max = heures_freqs[-1][0]
        self._timestamp_min = heures_freqs[0][0]
        self._etendue = self._timestamp_max - self._timestamp_min
        self._voies_sortantes = []
        self._voies_entrantes = []
        self._voies_sortantes_proba = {}

    def ajoute_voie_entrante(self, voies):
        self._voies_entrantes = voies
    
    def ajoute_voie_sortante(self, voies):
        self._voies_sortantes = voies
        for voie in self._voies_sortantes:
            self._voies_sortantes_proba[voie] = voie.proba_entree

    def notifie_temps(self, increment, moteur):
        print("Le generateur a ete modifie.")
        freq = 0
        if self._etendue == 0:
            freq = self._heures_freqs[0][1]
        else:
            timestamp = (moteur.temps % self.duree_journee) / self.duree_journee * self._etendue
            i = 0
            while self._heures_freqs[i+1][0] < timestamp:
                i+=1
            timestamp_gauche = self._heures_freqs[i][0]
            timestamp_droite = self._heures_freqs[i+1][0]
            fact_prop = (timestamp - timestamp_gauche) / (timestamp_droite - timestamp_gauche)
            freq_gauche = self._heures_freqs[i][1]
            freq_droite = self._heures_freqs[i+1][1]
            freq = freq_gauche + fact_prop * (freq_droite - freq_gauche)
        
        nombre_voit_crees = var_poisson(freq/(60*moteur.nombre_ticks_seconde), increment)
        print("Nombre de voitures : "+str(nombre_voit_crees))
        for i in range(nombre_voit_crees):
            longueur = normalvariate(428, 50)
            aggressivite = (random() < Vehicule.proportion_discourtois)

            probas = []
            for key in self._voies_sortantes_proba.keys():
                probas.append(self._voies_sortantes_proba.get(key))
            voie = numpy.random.choice(self._voies_sortantes, 1, False, probas)

            voie[0].creer_vehicule(aggressivite, longueur)



################################################
#          TESTS
################################################
#print('##### Tests #####')
#print('## Loi de poisson l = 1')
#for i in range(0, 5):
#    print(proba_poisson(i, 1, 1))
#
#print('## Loi de poisson l = 2')
#for i in range(0, 7):
#    print(proba_poisson(i, 2, 1))
#
#print('\n##Génération d\'une série de valeurs suivant une loi de Poisson de param. 1')
#R = []
#for i in range(0, 1000):
#    R.append(var_poisson(1, 1))
#
#print('\n##Génération d\'une série de valeurs suivant une loi de Poisson de param. 10')
#R = []
#for i in range(0, 1000):
#    R.append(var_poisson(1, 10))
#print(R)

