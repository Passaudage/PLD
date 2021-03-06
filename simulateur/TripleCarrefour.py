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
    gen1_sud = GenerateurEntrees.GenerateurEntrees([[1 , 1], [2, 5], [3, 10]])
    sm.add_listener(gen1_sud)
    gen1_ouest = GenerateurEntrees.GenerateurEntrees([[1 , 1], [2, 1], [3, 1]])
    sm.add_listener(gen1_ouest)
    
    gen2_sud = GenerateurEntrees.GenerateurEntrees([[1 , 1], [2, 5], [3, 10]])
    sm.add_listener(gen2_sud)
    gen2_est = GenerateurEntrees.GenerateurEntrees([[1 , 1], [2, 1], [3, 1]])
    sm.add_listener(gen2_est)

    gen3_ouest = GenerateurEntrees.GenerateurEntrees([[1 , 1], [2, 1], [3, 1]])
    sm.add_listener(gen3_ouest)
    gen3_nord = GenerateurEntrees.GenerateurEntrees([[1 , 10], [2, 5], [3, 1]])
    sm.add_listener(gen3_nord)

    gen4_est = GenerateurEntrees.GenerateurEntrees([[1 , 9], [2, 7], [3, 12]])
    sm.add_listener(gen4_est)
    gen4_nord = GenerateurEntrees.GenerateurEntrees([[1 , 10], [2, 5], [3, 1]])
    sm.add_listener(gen4_nord)

    # Intersections #
    i = Intersection.Intersection(sm,Coordonnees.Coordonnees(6050, 6050), 2100, 2100)
    sm.add_listener(i)
    i2 = Intersection.Intersection(sm,Coordonnees.Coordonnees(13150, 6050), 2100, 2100)
    sm.add_listener(i2)
    i3 = Intersection.Intersection(sm,Coordonnees.Coordonnees(6050, 13150), 2100, 2100)
    sm.add_listener(i3)
    i4 = Intersection.Intersection(sm,Coordonnees.Coordonnees(13150, 13150), 2100, 2100)
    sm.add_listener(i4)
    
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

    t1_nord = Troncon.Troncon(i3, i, Coordonnees.Coordonnees(6050, 7100), Coordonnees.Coordonnees(6050, longueur_troncon+7100),
                    {"G": 0.2, "TD": 0.4, "D": 0.4},
                    {"G": 0.3, "TD": 0.5, "D": 0.2})

    #t1_nord.ajouter_generateur("sens2",gen1_nord)
    
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
    
    t2_nord = Troncon.Troncon(i4, i2, Coordonnees.Coordonnees(13150, 7100), Coordonnees.Coordonnees(13150, longueur_troncon+7100),
                    {"G": 0.2, "TD": 0.4, "D": 0.4},
                    {"G": 0.3, "TD": 0.5, "D": 0.2})

       
    t3_est = Troncon.Troncon(i4, i3, Coordonnees.Coordonnees(7100, 13150), Coordonnees.Coordonnees(7100+longueur_troncon, 13150),
                    {"G": 0.2, "TD": 0.5, "D": 0.3},
                    {"G": 0.3, "TD": 0.2, "D": 0.5})

    
    t3_ouest = Troncon.Troncon(i3, None, Coordonnees.Coordonnees(0, 13150), Coordonnees.Coordonnees(longueur_troncon, 13150),
                    {"G": 0.5, "TD": 0.2, "D": 0.3},
                    {"G": 0.1, "TD": 0.7, "D": 0.2})

    t3_ouest.ajouter_generateur("sens1",gen3_ouest)

    t3_nord = Troncon.Troncon(None, i3, Coordonnees.Coordonnees(6050, 14200), Coordonnees.Coordonnees(6050, longueur_troncon+14200),
                    {"G": 0.2, "TD": 0.4, "D": 0.4},
                    {"G": 0.3, "TD": 0.5, "D": 0.2})

    t3_nord.ajouter_generateur("sens2",gen3_nord)

    t4_nord =Troncon.Troncon(None, i4, Coordonnees.Coordonnees(13150, 14200), Coordonnees.Coordonnees(13150, longueur_troncon+14200),
                             {"G": 0.2, "TD": 0.4, "D": 0.4},
                             {"G": 0.3, "TD": 0.5, "D": 0.2})

    t4_nord.ajouter_generateur("sens2", gen4_nord)

    t4_est = Troncon.Troncon(None, i4, Coordonnees.Coordonnees(14200, 13150), Coordonnees.Coordonnees(14200+longueur_troncon, 13150),
                             {"G": 0.2, "TD": 0.4, "D": 0.4},
                             {"G": 0.3, "TD": 0.5, "D": 0.2})

    t4_est.ajouter_generateur("sens2", gen4_est)
 
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
    t1_est.creer_voie(["TD"], "sens1", 1388)
    t1_est.creer_voie(["D"], "sens1", 1388)
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
    t2_est.creer_voie(["TD"], "sens1", 1388)
    t2_est.creer_voie(["D"], "sens1", 1388)
    t2_est.creer_voie(["G"], "sens2", 1388)
    t2_est.creer_voie(["TD"], "sens2", 1388)
    t2_est.creer_voie(["D"], "sens2", 1388)
      
      
    t3_ouest.creer_voie(["G"], "sens1", 1388)
    t3_ouest.creer_voie(["TD"], "sens1", 1388)
    t3_ouest.creer_voie(["D"], "sens1", 1388)
    t3_ouest.creer_voie(["G"], "sens2", 1388)
    t3_ouest.creer_voie(["TD"], "sens2", 1388)
    t3_ouest.creer_voie(["D"], "sens2", 1388)

    t3_nord.creer_voie(["G"], "sens1", 1388)
    t3_nord.creer_voie(["TD"], "sens1", 1388)
    t3_nord.creer_voie(["D"], "sens1", 1388)
    t3_nord.creer_voie(["G"], "sens2", 1388)
    t3_nord.creer_voie(["TD"], "sens2", 1388)
    t3_nord.creer_voie(["D"], "sens2", 1388)

    t3_est.creer_voie(["G"], "sens1", 1388)
    t3_est.creer_voie(["TD"], "sens1", 1388)
    t3_est.creer_voie(["D"], "sens1", 1388)
    t3_est.creer_voie(["G"], "sens2", 1388)
    t3_est.creer_voie(["TD"], "sens2", 1388)
    t3_est.creer_voie(["D"], "sens2", 1388)

    t4_est.creer_voie(["G"], "sens1", 1388)
    t4_est.creer_voie(["TD"], "sens1", 1388)
    t4_est.creer_voie(["D"], "sens1", 1388)
    t4_est.creer_voie(["G"], "sens2", 1388)
    t4_est.creer_voie(["TD"], "sens2", 1388)
    t4_est.creer_voie(["D"], "sens2", 1388)

    t4_nord.creer_voie(["G"], "sens1", 1388)
    t4_nord.creer_voie(["TD"], "sens1", 1388)
    t4_nord.creer_voie(["D"], "sens1", 1388)
    t4_nord.creer_voie(["G"], "sens2", 1388)
    t4_nord.creer_voie(["TD"], "sens2", 1388)
    t4_nord.creer_voie(["D"], "sens2", 1388)
    
    # Feux #
    i.creer_feux()
    i2.creer_feux()
    i3.creer_feux()
    i4.creer_feux()

    i.trouver_configurations_feux()
    i2.trouver_configurations_feux()
    i3.trouver_configurations_feux()
    i4.trouver_configurations_feux()
    
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
