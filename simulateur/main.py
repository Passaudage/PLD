import GenerateurEntrees
import Intersection
import SimulationManager
import Troncon
import Coordonnees


def charger_simulateur():
    longueur_troncon = 5000
    
    sm = SimulationManager.SimulationManager(5)
    gen_sud = GenerateurEntrees.GenerateurEntrees([[1 , 3], [2, 5], [3, 9]])
    sm.add_listener(gen_sud)
    gen_ouest = GenerateurEntrees.GenerateurEntrees([[1 , 3], [2, 5], [3, 9]])
    sm.add_listener(gen_ouest)
    gen_est = GenerateurEntrees.GenerateurEntrees([[1 , 3], [2, 5], [3, 9]])
    sm.add_listener(gen_est)
    gen_nord = GenerateurEntrees.GenerateurEntrees([[1 , 3], [2, 5], [3, 9]])
    sm.add_listener(gen_nord)

    i = Intersection.Intersection(Coordonnees.Coordonnees(6050, 6050), 2100, 2100)
    sm.add_listener(i)
    
    t_sud = Troncon.Troncon(i,
            None,
             Coordonnees.Coordonnees(6050, 0),
             Coordonnees.Coordonnees(6050, longueur_troncon),
                {"G" : 0.2 , "TD" : 0.5 , "D": 0.3},
                {"G": 0.3, "TD": 0.2, "D": 0.5})
    
    t_est = Troncon.Troncon(None, i, Coordonnees.Coordonnees(7100, 6050), Coordonnees.Coordonnees(7100+longueur_troncon, 6050),
                    {"G": 0.2, "TD": 0.5, "D": 0.3},
                    {"G": 0.3, "TD": 0.2, "D": 0.5})
    
    t_ouest = Troncon.Troncon(i, None, Coordonnees.Coordonnees(0, 6050), Coordonnees.Coordonnees(longueur_troncon, 6050),
                    {"G": 0.5, "TD": 0.2, "D": 0.3},
                    {"G": 0.1, "TD": 0.7, "D": 0.2})

    t_nord = Troncon.Troncon(None, i, Coordonnees.Coordonnees(6050, 7100), Coordonnees.Coordonnees(6050, longueur_troncon+7100),
                    {"G": 0.2, "TD": 0.4, "D": 0.4},
                    {"G": 0.3, "TD": 0.5, "D": 0.2})
 
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
    t_est.creer_voie(["TD", "G"], "sens1", 1388)
    t_est.creer_voie(["D", "TD"], "sens1", 1388)
    t_est.creer_voie(["G"], "sens2", 1388)
    t_est.creer_voie(["TD"], "sens2", 1388)
    t_est.creer_voie(["D"], "sens2", 1388)

    t_ouest.creer_voie(["G"], "sens1", 1388)
    t_ouest.creer_voie(["TD"], "sens1", 1388)
    t_ouest.creer_voie(["D"], "sens1", 1388)
    t_ouest.creer_voie(["G"], "sens2", 1388)
    t_ouest.creer_voie(["TD"], "sens2", 1388)
    t_ouest.creer_voie(["D"], "sens2", 1388)

    
    gen_sud.ajoute_voie_entrante(t_sud.voies_sens2)
    gen_est.ajoute_voie_entrante(t_est.voies_sens1)
    gen_ouest.ajoute_voie_entrante(t_ouest.voies_sens2)
    gen_nord.ajoute_voie_entrante(t_nord.voies_sens1)
    gen_sud.ajoute_voie_sortante(t_sud.voies_sens1)
    gen_est.ajoute_voie_sortante(t_est.voies_sens2)
    gen_ouest.ajoute_voie_sortante(t_ouest.voies_sens1)
    gen_nord.ajoute_voie_sortante(t_nord.voies_sens2)
    
    #~ print("Intersection")
    #~ print(i.coordonnees)
    #~ print("Troncon bas")
    #~ print(i.troncon_bas.coordonnees_debut)
    #~ print(i.troncon_bas.coordonnees_fin)
    #~ print("Troncon haut")
    #~ print(i.troncon_haut.coordonnees_debut)
    #~ print(i.troncon_haut.coordonnees_fin)
    #~ print("Troncon droite")
    #~ print(i.troncon_droite.coordonnees_debut)
    #~ print(i.troncon_droite.coordonnees_fin)
    #~ print("Troncon gauche")
    #~ print(i.troncon_gauche.coordonnees_debut)
    #~ print(i.troncon_gauche.coordonnees_fin)
    #~ 
    #~ if(i.construire_chemins()):
        #~ print("ca marche ! :D")
    #~ else : print("Ca marche pas ! :'(")
    
    return sm

def main():

    sm = charger_simulateur()

    print(sm.listeners)
    print()
    for i in range(15000):
        sm.avance_temps()
        #~ print()
        
    #~ print(Vehicule.count)
