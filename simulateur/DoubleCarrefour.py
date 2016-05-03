import GenerateurEntrees
import Intersection
import SimulationManager
import Troncon
import Coordonnees
import Vehicule


def charger_simulateur():
    longueur_troncon = 5000 
    
    # Manager #
    sm = SimulationManager.SimulationManager(5)
	
	# Générateurs #
    gen1_sud = GenerateurEntrees.GenerateurEntrees([[1 , 30], [2, 30], [3, 10]])
    sm.add_listener(gen1_sud)
    gen1_ouest = GenerateurEntrees.GenerateurEntrees([[1 , 4], [2, 7], [3, 10]])
    sm.add_listener(gen1_ouest)
    gen1_nord = GenerateurEntrees.GenerateurEntrees([[1 , 9], [2, 8], [3, 10]])
    sm.add_listener(gen1_nord)
    
    gen2_sud = GenerateurEntrees.GenerateurEntrees([[1 , 3], [2, 5], [3, 9]])
    sm.add_listener(gen2_sud)
    gen2_est = GenerateurEntrees.GenerateurEntrees([[1 , 3], [2, 5], [3, 9]])
    sm.add_listener(gen2_est)
    gen2_nord = GenerateurEntrees.GenerateurEntrees([[1 , 3], [2, 5], [3, 9]])
    sm.add_listener(gen2_nord)
    
	# Intersections #
    i = Intersection.Intersection(sm, Coordonnees.Coordonnees(6050, 6050), 2100, 2100)
    sm.add_listener(i)
    i2 = Intersection.Intersection(sm, Coordonnees.Coordonnees(13150, 6050), 2100, 2100)
    sm.add_listener(i2)
    
    # Tronçons #    
    t1_sud = Troncon.Troncon(i,
            None,
             Coordonnees.Coordonnees(6050, 0),
             Coordonnees.Coordonnees(6050, longueur_troncon),
                {"G" : 0.2 , "TD" : 0.5 , "D": 0.3},
                {"G": 0.3, "TD": 0.2, "D": 0.5})
                
    t1_sud.ajouter_generateur("sens1",gen1_sud)
    
    t1_est = Troncon.Troncon(i2, i, Coordonnees.Coordonnees(7100, 6050), Coordonnees.Coordonnees(7100+longueur_troncon, 6050),
                    {"G": 0.2, "TD": 0.5, "D": 0.3},
                    {"G": 0.3, "TD": 0.2, "D": 0.5})

    
    t1_ouest = Troncon.Troncon(i, None, Coordonnees.Coordonnees(0, 6050), Coordonnees.Coordonnees(longueur_troncon, 6050),
                    {"G": 0.5, "TD": 0.2, "D": 0.3},
                    {"G": 0.1, "TD": 0.7, "D": 0.2})

    t1_ouest.ajouter_generateur("sens1",gen1_ouest)

    t1_nord = Troncon.Troncon(None, i, Coordonnees.Coordonnees(6050, 7100), Coordonnees.Coordonnees(6050, longueur_troncon+7100),
                    {"G": 0.2, "TD": 0.4, "D": 0.4},
                    {"G": 0.3, "TD": 0.5, "D": 0.2})

    t1_nord.ajouter_generateur("sens2",gen1_nord)
    
    t2_sud = Troncon.Troncon(i2,
            None,
             Coordonnees.Coordonnees(13150, 0),
             Coordonnees.Coordonnees(13150, longueur_troncon),
                {"G" : 0.2 , "TD" : 0.5 , "D": 0.3},
                {"G": 0.3, "TD": 0.2, "D": 0.5})
                
    t2_sud.ajouter_generateur("sens1",gen2_sud)
    
    t2_est = Troncon.Troncon(None, i2, Coordonnees.Coordonnees(14200, 6050), Coordonnees.Coordonnees(14200+longueur_troncon, 6050),
                    {"G": 0.2, "TD": 0.5, "D": 0.3},
                    {"G": 0.3, "TD": 0.2, "D": 0.5})

    t2_est.ajouter_generateur("sens2",gen2_est)
    
    t2_nord = Troncon.Troncon(None, i2, Coordonnees.Coordonnees(13150, 7100), Coordonnees.Coordonnees(13150, longueur_troncon+7100),
                    {"G": 0.2, "TD": 0.4, "D": 0.4},
                    {"G": 0.3, "TD": 0.5, "D": 0.2})

    t2_nord.ajouter_generateur("sens2",gen2_nord)
 
	# Voies #
    t1_sud.creer_voie(["G"], "sens1", 1388)
    t1_sud.creer_voie(["TD"], "sens1", 1388)
    t1_sud.creer_voie(["D"], "sens1", 1388)
    t1_sud.creer_voie(["G"], "sens2", 1388)
    t1_sud.creer_voie(["TD"], "sens2", 1388)
    t1_sud.creer_voie(["D"], "sens2", 1388)

    t1_nord.creer_voie(["G"], "sens1", 1388)
    t1_nord.creer_voie(["TD"], "sens1", 1388)
    t1_nord.creer_voie(["D"], "sens1", 1388)
    t1_nord.creer_voie(["G"], "sens2", 1388)
    t1_nord.creer_voie(["TD"], "sens2", 1388)
    t1_nord.creer_voie(["D"], "sens2", 1388)

    t1_est.creer_voie(["G"], "sens1", 1388)
    t1_est.creer_voie(["TD", "G"], "sens1", 1388)
    t1_est.creer_voie(["D", "TD"], "sens1", 1388)
    t1_est.creer_voie(["G"], "sens2", 1388)
    t1_est.creer_voie(["TD"], "sens2", 1388)
    t1_est.creer_voie(["D"], "sens2", 1388)

    t1_ouest.creer_voie(["G"], "sens1", 1388)
    t1_ouest.creer_voie(["TD"], "sens1", 1388)
    t1_ouest.creer_voie(["D"], "sens1", 1388)
    t1_ouest.creer_voie(["G"], "sens2", 1388)
    t1_ouest.creer_voie(["TD"], "sens2", 1388)
    t1_ouest.creer_voie(["D"], "sens2", 1388)
    
    t2_sud.creer_voie(["G"], "sens1", 1388)
    t2_sud.creer_voie(["TD"], "sens1", 1388)
    t2_sud.creer_voie(["D"], "sens1", 1388)
    t2_sud.creer_voie(["G"], "sens2", 1388)
    t2_sud.creer_voie(["TD"], "sens2", 1388)
    t2_sud.creer_voie(["D"], "sens2", 1388)

    t2_nord.creer_voie(["G"], "sens1", 1388)
    t2_nord.creer_voie(["TD"], "sens1", 1388)
    t2_nord.creer_voie(["D"], "sens1", 1388)
    t2_nord.creer_voie(["G"], "sens2", 1388)
    t2_nord.creer_voie(["TD"], "sens2", 1388)
    t2_nord.creer_voie(["D"], "sens2", 1388)

    t2_est.creer_voie(["G"], "sens1", 1388)
    t2_est.creer_voie(["TD", "G"], "sens1", 1388)
    t2_est.creer_voie(["D", "TD"], "sens1", 1388)
    t2_est.creer_voie(["G"], "sens2", 1388)
    t2_est.creer_voie(["TD"], "sens2", 1388)
    t2_est.creer_voie(["D"], "sens2", 1388)
    
    # Feux #
    i.creer_feux()
    i2.creer_feux()
    
    i.trouver_configurations_feux()
    i2.trouver_configurations_feux()

#    t2_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
#    t2_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
#    t2_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
#    t2_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
#    t2_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
#    
#    t2_nord.voies_sens2[2].creer_vehicule(sm, 0, 500)
#    t2_nord.voies_sens2[2].creer_vehicule(sm, 0, 500)
#    t2_nord.voies_sens2[2].creer_vehicule(sm, 0, 500)
#    t2_nord.voies_sens2[2].creer_vehicule(sm, 0, 500)
#    t2_nord.voies_sens2[2].creer_vehicule(sm, 0, 500)
#    
#    t2_sud.voies_sens1[0].creer_vehicule(sm, 0, 500)
#    t2_sud.voies_sens1[0].creer_vehicule(sm, 0, 500)
#    t2_sud.voies_sens1[0].creer_vehicule(sm, 0, 500)
#    t2_sud.voies_sens1[0].creer_vehicule(sm, 0, 500)
#    t2_sud.voies_sens1[0].creer_vehicule(sm, 0, 500)
#    
#    t2_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
#    t2_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
#    t2_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
#    t2_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
#    t2_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
#    
#    t2_nord.voies_sens2[2].creer_vehicule(sm, 0, 500)
#    t2_nord.voies_sens2[2].creer_vehicule(sm, 0, 500)
#    t2_nord.voies_sens2[2].creer_vehicule(sm, 0, 500)
#    t2_nord.voies_sens2[2].creer_vehicule(sm, 0, 500)
#    t2_nord.voies_sens2[2].creer_vehicule(sm, 0, 500)
#    
#    t2_sud.voies_sens1[0].creer_vehicule(sm, 0, 500)
#    t2_sud.voies_sens1[0].creer_vehicule(sm, 0, 500)
#    t2_sud.voies_sens1[0].creer_vehicule(sm, 0, 500)
#    t2_sud.voies_sens1[0].creer_vehicule(sm, 0, 500)
#    t2_sud.voies_sens1[0].creer_vehicule(sm, 0, 500)

    return sm
