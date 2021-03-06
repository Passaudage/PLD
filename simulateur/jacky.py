import GenerateurEntrees
import Intersection
import SimulationManager
import Troncon
import Coordonnees
import Vehicule


def charger_simulateur():
    longueur_troncon = 5000
    
    sm = SimulationManager.SimulationManager(5)
    gen_sud = GenerateurEntrees.GenerateurEntrees([[1 , 20]])
    sm.add_listener(gen_sud)
    gen_ouest = GenerateurEntrees.GenerateurEntrees([[1 , 3]])
    sm.add_listener(gen_ouest)
    gen_est = GenerateurEntrees.GenerateurEntrees([[1 , 5]])
    sm.add_listener(gen_est)
    gen_nord = GenerateurEntrees.GenerateurEntrees([[1 , 3]])
    sm.add_listener(gen_nord)

    i = Intersection.Intersection(sm, Coordonnees.Coordonnees(6050, 6050), 2100, 2100)
    sm.add_listener(i)
    
    t_sud = Troncon.Troncon(i,
            None,
             Coordonnees.Coordonnees(6050, 0),
             Coordonnees.Coordonnees(6050, longueur_troncon),
                {"G" : 0.2 , "TD" : 0.5 , "D": 0.3},
                {"G": 0.3, "TD": 0.2, "D": 0.5})
                
    t_sud.ajouter_generateur("sens1",gen_sud)
    
    t_est = Troncon.Troncon(None, i, Coordonnees.Coordonnees(7100, 6050), Coordonnees.Coordonnees(7100+longueur_troncon, 6050),
                    {"G": 0.2, "TD": 0.5, "D": 0.3},
                    {"G": 0.3, "TD": 0.2, "D": 0.5})

    t_est.ajouter_generateur("sens2",gen_est)
    
    t_ouest = Troncon.Troncon(i, None, Coordonnees.Coordonnees(0, 6050), Coordonnees.Coordonnees(longueur_troncon, 6050),
                    {"G": 0.5, "TD": 0.2, "D": 0.3},
                    {"G": 0.1, "TD": 0.7, "D": 0.2})

    t_ouest.ajouter_generateur("sens1",gen_ouest)

    t_nord = Troncon.Troncon(None, i, Coordonnees.Coordonnees(6050, 7100), Coordonnees.Coordonnees(6050, longueur_troncon+7100),
                    {"G": 0.2, "TD": 0.4, "D": 0.4},
                    {"G": 0.3, "TD": 0.5, "D": 0.2})

    t_nord.ajouter_generateur("sens2",gen_nord)
 
    t_sud.creer_voie(["G"], "sens1", 1388)
    t_sud.creer_voie(["TD"], "sens1", 1388)
    t_sud.creer_voie(["D"], "sens1", 1388)
    t_sud.creer_voie(["G"], "sens2", 1388)
    t_sud.creer_voie(["TD"], "sens2", 1388)
    t_sud.creer_voie(["D"], "sens2", 1388)

    t_nord.creer_voie(["G"], "sens1", 1388)
    t_nord.creer_voie(["TD"], "sens1", 1388)
    t_nord.creer_voie(["D"], "sens1", 1388)
    t_nord.creer_voie(["G"], "sens2", 1388)
    t_nord.creer_voie(["TD"], "sens2", 1388)
    t_nord.creer_voie(["D"], "sens2", 1388)

    t_est.creer_voie(["G"], "sens1", 1388)
    t_est.creer_voie(["TD"], "sens1", 1388)
    t_est.creer_voie(["D"], "sens1", 1388)
    t_est.creer_voie(["G"], "sens2", 1388)
    t_est.creer_voie(["TD"], "sens2", 1388)
    t_est.creer_voie(["D"], "sens2", 1388)

    t_ouest.creer_voie(["G"], "sens1", 1388)
    t_ouest.creer_voie(["TD"], "sens1", 1388)
    t_ouest.creer_voie(["D"], "sens1", 1388)
    t_ouest.creer_voie(["G"], "sens2", 1388)
    t_ouest.creer_voie(["TD"], "sens2", 1388)
    t_ouest.creer_voie(["D"], "sens2", 1388)
    
    t_ouest.donner_voies_intersections()
    t_est.donner_voies_intersections()
    t_nord.donner_voies_intersections()
    t_sud.donner_voies_intersections()

    i.creer_feux()
    #~ gen_sud.ajoute_voie_entrante(t_sud.voies_sens2)
    #~ gen_est.ajoute_voie_entrante(t_est.voies_sens1)
    #~ gen_ouest.ajoute_voie_entrante(t_ouest.voies_sens2)
    #~ gen_nord.ajoute_voie_entrante(t_nord.voies_sens1)
    #~ gen_sud.ajoute_voie_sortante(t_sud.voies_sens1)
    #~ gen_est.ajoute_voie_sortante(t_est.voies_sens2)
    #~ gen_ouest.ajoute_voie_sortante(t_ouest.voies_sens1)
    #~ gen_nord.ajoute_voie_sortante(t_nord.voies_sens2)
    
    #~ t_est.voies_sens2[0].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[2].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[0].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[2].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[0].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[2].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[0].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[2].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[0].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[2].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[0].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[2].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[0].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[2].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[0].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[1].creer_vehicule(sm, 0, 500)
    #~ t_est.voies_sens2[2].creer_vehicule(sm, 0, 500)
    #~ 

    i.trouver_configurations_feux()

    #~ print(i.combinaisons)
    #for k,v in i.combinaisons.items():
    #    print(str(k)+" "+str(v))
    #    for f in v:
    #        print("feu " + str(f[0])) 
    #raise Exception("Bonfante")
   
    return sm

def main():

    a = Coordonnees.Coordonnees(0,1)
    b = a
    a = a + a
    print(a + b)

    sm = charger_simulateur()
    
    liste_v = Vehicule.Vehicule.liste_voitures
    #print(liste_v)
    
    toto = liste_v[0]
    #print(toto.origine)

    #~ toto.notifie_temps(5,sm)
    #~ toto.notifie_temps(5,sm)
    #~ toto.notifie_temps(5,sm)
    #~ toto.notifie_temps(5,sm)
    #~ toto.notifie_temps(5,sm)
    #~ for i in range(10000):
        #~ sm.avance_temps()

    toto = liste_v[0]
    #print(toto.intersection)

    
        
    for v in liste_v:
        print(v.coordonnees)
        pass
   
        
if __name__ == '__main__':
    main()
