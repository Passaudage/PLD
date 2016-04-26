import SimulationManager
from math import *
import random

def proba_poisson(k, freq, temps_obs):
        #Calcul du lambda correspondant
        l = freq * temps_obs
        p = e ** (-l)
        for i in range(0, k):
            p *= l/k
            k = k-1
        return p

def var_poisson(freq, temps_obs):
    proba_cumulee = random.random()
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
        self._etendue = self.timestamp_max - self.timestamp_min

    def notifie_temps(self, increment, moteur):
        freq = 0
        if self.etendue == 0:
            freq = self.heures_freqs[0][1]
        else:
            timestamp = (moteur.temps % duree_journee) / duree_journee * etendue
            i = 0
            while self.heures_freqs[i+1][0] < timestamp:
                i+=1
            timestamp_gauche = self.heures_freqs[i][0]
            timestamp_droite = self.heures_freqs[i+1][0]
            fact_prop = (timestamp - timestamp_gauche) / (timestamp_droite - timestamp_gauche)
            freq_gauche = self.heures_freqs[i][1]
            freq_droite = self.heures_freqs[i+1][1]
            freq = freq_gauche + fact_prop * (freq_droite - freq_gauche)
        
        nombre_voit_crees = var_poisson(freq/(60*moteur.nombre_ticks_seconde), increment)
        



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
