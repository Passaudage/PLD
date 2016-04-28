from Coordonnees import *
from Feu import *
from GenerateurEntrees import *
from Intersection import *
from SimulationManager import *
from Troncon import *
from Vehicule import *
from Voie import *


def main():
    longueur_troncon = 5000
    
    sm = SimulationManager(5)
    gen_sud = GenerateurEntrees([1, 2, 3, 4, 5, 6, 7])
    gen_ouest = GenerateurEntrees([1, 2, 3, 4, 5, 6, 7])
    gen_est = GenerateurEntrees([1, 2, 3, 4, 5, 6, 7])
    gen_nord = GenerateurEntrees([1, 2, 3, 4, 5, 6, 7])

    i = Intersection.Intersection(Coordonnees.Coordonnees(6050, 6050))
    
    t_sud = Troncon(i, None, Coordonnees.Coordonnees(6050, 0), Coordonnees.Coordonnees(6050, longueur_troncon),
                {"G" : 0.2 , "TD" : 0.5 , "D": 0.3}, {"G": 0.3, "TD": 0.2, "D": 0.5})

    t_est = Troncon(None, i, Coordonnees.Coordonnees(7100, 6050), Coordonnees.Coordonnees(7100+longueur_troncon, 6050),
                    {"G": 0.2, "TD": 0.5, "D": 0.3},
                    {"G": 0.3, "TD": 0.2, "D": 0.5})
    
    t_ouest = Troncon(i, None, Coordonnees.Coordonnees(0, 6050), Coordonnees.Coordonnees(longueur_troncon, 6050),
                    {"G": 0.5, "TD": 0.2, "D": 0.3},
                    {"G": 0.1, "TD": 0.7, "D": 0.2})

    t_nord = Troncon(None, i, Coordonnees.Coordonnees(6050, 7100), Coordonnees.Coordonnees(6050, longueur_troncon+7100),
                    {"G": 0.2, "TD": 0.4, "D": 0.4},
                    {"G": 0.3, "TD": 0.5, "D": 0.2})
    
    t_sud.creer_voie(["G"], "sens1", 50)
    t_sud.creer_voie(["TD"], "sens1", 50)
    t_sud.creer_voie(["D"], "sens1", 50)
    t_sud.creer_voie(["G"], "sens2", 50)
    t_sud.creer_voie(["TD"], "sens2", 50)
    t_sud.creer_voie(["D"], "sens2", 50)

    t_nord.creer_voie(["G"], "sens1", 50)
    t_nord.creer_voie(["TD"], "sens1", 50)
    t_nord.creer_voie(["D"], "sens1", 50)
    t_nord.creer_voie(["G"], "sens2", 50)
    t_nord.creer_voie(["TD"], "sens2", 50)
    t_nord.creer_voie(["D"], "sens2", 50)

    t_est.creer_voie(["G"], "sens1", 50)
    t_est.creer_voie(["TD", "G"], "sens1", 50)
    t_est.creer_voie(["D", "TD"], "sens1", 50)
    t_est.creer_voie(["G"], "sens2", 50)
    t_est.creer_voie(["TD"], "sens2", 50)
    t_est.creer_voie(["D"], "sens2", 50)

    t_ouest.creer_voie(["G"], "sens1", 50)
    t_ouest.creer_voie(["TD"], "sens1", 50)
    t_ouest.creer_voie(["D"], "sens1", 50)
    t_ouest.creer_voie(["G"], "sens2", 50)
    t_ouest.creer_voie(["TD"], "sens2", 50)
    t_ouest.creer_voie(["D"], "sens2", 50)

    for voie in t_sud.voies_sens2:
        gen_sud.ajoute_voie_entrante(voie)

    for voie in t_est.voies_sens1:
        gen_est.ajoute_voie_entrante(voie)

    for voie in t_ouest.voies_sens2:
        gen_ouest.ajoute_voie_entrante(voie)

    for voie in t_nord.voies_sens1:
        gen_nord.ajoute_voie_entrante(voie)

    for voie in t_sud.voies_sens1:
        gen_sud.ajoute_voie_sortante(voie)

    for voie in t_est.voies_sens2:
        gen_est.ajoute_voie_sortante(voie)

    for voie in t_ouest.voies_sens1:
        gen_ouest.ajoute_voie_sortante(voie)

    for voie in t_nord.voies_sens2:
        gen_nord.ajoute_voie_sortante(voie)
    
    
    
    
    
    
    