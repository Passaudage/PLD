import Feu
import Coordonnees
import Vehicule
import time
import SimulationManager
import GestionnaireFeux

def min_liste_coord(liste, y = True):
    element_min = None
    for element in liste:
        if element_min is None:
            element_min = element
        elif (y and element.y < element_min.y) or ((not y) and element.x < element_min.x):
                element_min = element
    return element_min

class Intersection:
    """
        Modelise une intersection.
            # coordonees : Position de l'intersection sur la grille
            # sur_place : Dictionnaire utilisé pour résoudre les interblocages
            # qui arrivent parfois lorsque deux voitures se rencontrent perpendiculairement
            # (des histoires d'arrondi...)
            # @author : Bonfante
    """
    duree_minimum_feu = 10 * SimulationManager.SimulationManager.nombre_ticks_seconde # secondes * nb_ticks_par_second
    vitesse_max = 555 # cm.s^{-1}
    sur_place = {}
    
    def __init__(self, simulateur, coordonnees, hauteur, largeur):
        self.simulateur = simulateur
        
        # Map combinaisons
        self.combinaisons = {}
        
        # Position du point central de l'intersection
        self.coordonnees = coordonnees
        self.hauteur = hauteur
        self.largeur = largeur
        self.timestamp_maj = 0
        
        # Troncon gauche
        self.troncon_gauche = None
        
        # Troncon droite
        self.troncon_droite = None
        
        # Troncon haut
        self.troncon_haut = None
        
        # Troncon bas
        self.troncon_bas = None 
        
        # Feux agissant sur l'intersection
        self.feux = {}  
        
        # Voies sortantes
        self.sortantes = []

        # Voies entrantes
        self.entrantes = []
        
        # Voitures
        self.vehicules = []
        
        # Probas
        self.proba_haut = 0.3
        self.proba_bas = 0.3
        self.proba_droite = 0.2
        self.proba_gauche = 0.2
        
        # Chemins voitures
        # Map voiture/Liste de points restant à passer
        self.chemins_voitures = {}


        

    def get_proba(self, troncon, direction):
        if(troncon == self.troncon_gauche):
            somme = self.proba_haut+self.proba_droite+self.proba_bas
            if(direction =="D"):
                return self.proba_bas/somme
            elif(direction =="G"):
                return self.proba_haut/somme
            elif(direction == "TD"):
                return self.proba_droite/somme
            else:
                raise Exception("La direction n'est pas valide.")
        elif(troncon == self.troncon_droite):
            somme = self.proba_gauche+self.proba_haut+self.proba_bas
            if(direction =="D"):
                return self.proba_haut/somme
            elif(direction =="G"):
                return self.proba_bas/somme
            elif(direction == "TD"):
                return self.proba_gauche/somme
            else:
                raise Exception("La direction n'est pas valide.")
        elif(troncon == self.troncon_haut):
            somme = self.proba_gauche+self.proba_droite+self.proba_bas
            if(direction =="D"):
                return self.proba_gauche/somme
            elif(direction =="G"):
                return self.proba_droite/somme
            elif(direction == "TD"):
                return self.proba_bas/somme
            else:
                raise Exception("La direction n'est pas valide.")   
        elif(troncon == self.troncon_bas):
            somme = self.proba_gauche+self.proba_droite+self.proba_haut
            if(direction =="D"):
                return self.proba_droite/somme
            elif(direction =="G"):
                return self.proba_gauche/somme
            elif(direction == "TD"):
                return self.proba_haut/somme
            else:
                raise Exception("La direction n'est pas valide.")
        else:
            raise Exception("Le troncon n'existe pas dans l'intersection.")
        
    def branche_troncon(self, troncon, position):
        """
            Permet de connecter un troncon a l'intersection
                # Troncon : Le troncon a connecter.
                # Position : La position du troncon sur l'intersection 
                #           H haut, B bas, G gauche, D droite
                #         |    1  |
                #         |  Haut |
                # --------         --------
                # Gauche 2          Droite 0
                # --------         --------
                #         |  Bas  |
                #         |   3   |
                # @author : Bonfante
        """
        if(position=='G'):
            if(self.troncon_gauche != None):
                raise Exception("Troncon deja ajoute a gauche.")
            # Ajoute les voies entrantes et sortantes
            self.entrantes += troncon.voies_sens1
            self.sortantes += troncon.voies_sens2
            
            # Ajoute le troncon
            self.troncon_gauche = troncon
            
        elif(position=='B'):
            if(self.troncon_bas != None):
                raise Exception("Troncon deja ajoute en bas.")
            # Ajoute les voies entrantes et sortantes
            self.entrantes += troncon.voies_sens1
            self.sortantes += troncon.voies_sens2
            
            # Ajoute le troncon
            self.troncon_bas = troncon
            
        elif(position=='D'):
            if(self.troncon_droite != None):
                raise Exception("Troncon deja ajoute a droite.")
            # Ajoute les voies entrantes et sortantes
            self.entrantes += troncon.voies_sens2
            self.sortantes += troncon.voies_sens1
            
            # Ajoute le troncon
            self.troncon_droite = troncon
            
        elif(position=='H'):
            if(self.troncon_haut != None):
                raise Exception("Troncon deja ajoute en haut.")
            # Ajoute les voies entrantes et sortantes
            self.entrantes += troncon.voies_sens2
            self.sortantes += troncon.voies_sens1
            
            # Ajoute le troncon
            self.troncon_haut = troncon

        else:
            raise Exception(position+" n'est pas une direction convenable.")

    def creer_feux(self):
        self._creer_feux_troncon("sens1", self.troncon_bas, self.troncon_bas.voies_sens1, 3)
        self._creer_feux_troncon("sens2", self.troncon_haut, self.troncon_haut.voies_sens2, 1)
        self._creer_feux_troncon("sens1", self.troncon_gauche, self.troncon_gauche.voies_sens1, 2)
        self._creer_feux_troncon("sens2", self.troncon_droite, self.troncon_droite.voies_sens2, 0)

        print("feux du troncon bas")
        self.troncon_bas.afficher_feux()

        print("feux du troncon haut")
        self.troncon_haut.afficher_feux()

        print("feux du troncon gauche")
        self.troncon_gauche.afficher_feux()

        print("feux du troncon droite")
        self.troncon_droite.afficher_feux()

    def appliquer_configuration(self, numero_config, timestamp):
        configuration = self.combinaisons[numero_config]
        
        allfeux     = {feu for _, feu in self.feux.items()}
        feuxconfig  = {feu for _, feu in configuration}
        feuachanger = {feu for feu in allfeux if (feu in feuxconfig and not feu.passant)
                                                 or (feu not in feuxconfig and feu.passant)
                             }
        
        for feu in feuachanger:
            feu.change_couleur(timestamp)


    def _creer_feux_troncon(self, sens, troncon, voies_entrantes, offset):
        """
            Permet d'ajouter aux voies entrantes un feu
                # voies_entrantes : les voies entrantes
                # offset : la position des voies sur le carrefour
                            0 si D, 1 si H, 2 si G et 3 si B
                # @author : Bonfante
        """
        # Pour toutes les voies entrantes
        for voie in voies_entrantes:
            # Pour toutes les directions d'une voie entrante
            for direction in voie.directions:
                # On choisit le bon feu
                if(direction == "D"):
                    index = 2+3*offset
                elif(direction == "G"):
                    index = 0+3*offset
                elif(direction == "TD"):
                    index = 1+3*offset
                # Si le feu existe 
                if(index in self.feux.keys()):
                    feu = self.feux[index]
                # Si le feu n'existe pas
                else:
                    if(index in [0,1,2,6,7,8]):
                        sens_feu = 0
                    else:
                        sens_feu = 1
                    feu = Feu.Feu(self, sens_feu)
                    self.feux[index] = feu
                # On ajoute le feu a ce troncon
                troncon.ajouter_feux(sens,direction, feu)

    def dec2bin(d,nb=0):

        """
            dec2bin(d,nb=0): conversion nombre entier positif ou nul -> chaîne binaire (si nb>0, complète à gauche par des zéros)
        """
        if d==0:
            b="0"
        else:
            b=""
            while d!=0:
                b="01"[d&1]+b
                d=d>>1
        return b.zfill(nb)


    def trouver_configurations_feux(self):
        """
            renvoie toutes les combinaisons possibles de feus
            # @author : marcus
        """
        index = 0
        configuration = None
        # Pour toutes les configurations
        for i in range(4096):
        #~ for i in range(5):
            configuration = Intersection.dec2bin(i,12)
            # Si la configuration est correcte
            if(self.correcte(configuration)):
                # On ajoute les feux à rendre passant
                liste_feux = []
                for j in range(len(configuration)):
                    if(configuration[j] == '1'):
                        liste_feux.append((j,self.feux[j]))
                # on ajoute la combinaison à la map
                self.combinaisons[index] = liste_feux

                index +=1

        self.gestionnaire = GestionnaireFeux.gestionnaireDefaut()(len(self.combinaisons))


    def correcte(self,config):
        """
            renvoie vrai si la configuration est correcte
            @author : marcus
        """
        coupe = False
        liste_points = []
        index = 0
        for c in config:
            if(c=='1'):
                (d1,f1,d2,f2) = self.trouver_coordonnees_feu(index)
                liste_points.append((d1,f1))
                if(d2 is not None):
                    liste_points.append((d2,f2))
            index += 1

        for points1 in liste_points:
            for points2 in liste_points:
                if(points1 != points2):
                    if(Coordonnees.Coordonnees.se_coupent(points1[0], points1[1], points2[0], points2[1])):
                        return False
        return True
        
        
        
    def trouver_coordonnees_feu(self, numero):
        """
            retourne la où les droites correspondant à un feu
            # numero : numéro du feu dans l'intersection
            # @author : marcus
        """
        voie1 = None
        voie2 = None
        
        if(numero < 3):
            voies = self.troncon_bas.voies_sens1
        elif(numero<6):
            voies = self.troncon_droite.voies_sens2
            numero-=3
        elif(numero<9):
            voies = self.troncon_haut.voies_sens2
            numero-=6
        elif(numero<12):
            voies = self.troncon_gauche.voies_sens1
            numero-=9
            
        if(numero==0):
            for v in voies:
                if(v.direction_possible('G')):
                    voie1 = v
                    pass
            return(voie1.coordonnees_fin, self.demander_voies_sorties(voie1, 'G').coordonnees_debut, None, None)
        elif(numero==1):
            if(voies[0].direction_possible('TD')):
                voie1 = voies[0]
            if(voies[2].direction_possible('TD')):
                voie2 = voies[2]
            if(voie1 is None):
                voie1 = voies[1]
            if(voie2 is None):
                d2 = None
                f2 =None
            else:
                d2=voie2.coordonnees_fin
                f2=self.demander_voies_sorties(voie2, 'TD').coordonnees_debut
            return(voie1.coordonnees_fin, self.demander_voies_sorties(voie1, 'TD').coordonnees_debut, d2, f2)
            #~ for v in voies:
                #~ if(v.direction_possible('TD')):
                    #~ voie1 = v
                    #~ break
            #~ return(voie1.coordonnees_fin, self.demander_voies_sorties(voie1, 'TD').coordonnees_debut, None, None)
        elif(numero==2):
            for v in voies[::-1]:
                if(v.direction_possible('D')):
                    voie1 = v
                    pass
            return(voie1.coordonnees_fin, self.demander_voies_sorties(voie1, 'D').coordonnees_debut, None, None)
            

    def lister_troncon(self):
        return [self.troncon_gauche,self.troncon_haut,self.troncon_droite,self.troncon_bas]
                
    def demander_voies_sorties(self,voie_entree,direction):
        """
            Trouve les voies de sorties possibles si l'on
            arrive sur la voie voie_entree en direction de
            la direction passe en parametre
                # voie_entree : voie d'origine
                # direction : la direction ou l'on va
                # @author : Bonfante
        """

        # Si la voie est dans le troncon gauche

        troncon = voie_entree.troncon
        if(troncon==self.troncon_bas):
            index= self.troncon_bas.voies_sens1.index(voie_entree)
            if(direction == 'D'):
                return self.troncon_droite.voies_sens1[index]
            elif(direction == 'G'):
                return self.troncon_gauche.voies_sens2[index]
            elif(direction == 'TD'):
                return self.troncon_haut.voies_sens1[index]

        elif(troncon==self.troncon_haut):
            index = self.troncon_haut.voies_sens2.index(voie_entree)
            if(direction == 'D'):
                return self.troncon_gauche.voies_sens2[index]
            elif(direction == 'G'):
                return self.troncon_droite.voies_sens1[index]
            elif(direction == 'TD'):
                return self.troncon_bas.voies_sens2[index]


        elif(troncon == self.troncon_droite):
            index = self.troncon_droite.voies_sens2.index(voie_entree)
            if(direction == 'D'):
                return self.troncon_haut.voies_sens1[index]
            elif(direction == 'G'):
                return self.troncon_bas.voies_sens2[index]
            elif(direction == 'TD'):
                return self.troncon_gauche.voies_sens2[index]

        elif(troncon == self.troncon_gauche):
            index = self.troncon_gauche.voies_sens1.index(voie_entree)
            if(direction == 'D'):
                return self.troncon_bas.voies_sens2[index]
            elif(direction == 'G'):
                return self.troncon_haut.voies_sens1[index]
            elif(direction == 'TD'):
                return self.troncon_droite.voies_sens1[index]


    def ajouter_vehicule(self, vehicule):
        self.vehicules.append(vehicule)

    def retirer_vehicule(self, vehicule):
        self.vehicules.remove(vehicule)

    def donner_obstacle(self, voiture, coord, direction):
        coordonnees_blocage = None
        distance_blocage = 0
        vehicule_blocant = None

        largeur = Vehicule.Vehicule.largeur
        demi_largeur = largeur / 2

        vecteur_repere_x = Coordonnees.Coordonnees(direction.y, - direction.x)

        #print("@qlabernia : len(vehicules)=" + str(len(self.vehicules)))
        #print("-> Voiture référence : " + str(voiture))
        #print("   pos : " + str(coord))
        #print("   dir : " + str(direction))

        for vehicule in self.vehicules :

            if vehicule == voiture:
                continue

            cur_pos = vehicule.coordonnees # position du nez de la voiture
            cur_dir = vehicule.direction # orientation de la voiture
            cur_long = vehicule.longueur

            cur_intersection = None

            liste_points_rep = []

            points_gauche = []
            points_milieu = []
            points_droite = []

            # changement de repère

            cur_vecteur_repere_x = Coordonnees.Coordonnees(cur_dir.y, - cur_dir.x)

            point_1 = cur_pos + cur_vecteur_repere_x * demi_largeur
            point_2 = cur_pos - cur_vecteur_repere_x * demi_largeur
            point_3 = vehicule.donner_arriere() + cur_vecteur_repere_x * demi_largeur
            point_4 = vehicule.donner_arriere() - cur_vecteur_repere_x * demi_largeur

            # déterminer les quatres points : set à gauche, milieu, droite
            # on ne considère par les points si tous les y sont < -longueur_voiture

            tous_y_derriere_vehicule = True
            tous_y_devant_vehicule_blocant = True
            un_y_devant_vehicule = False

            for point in [point_1, point_2, point_3, point_4]:
                point_rep = Coordonnees.Coordonnees.changer_repere(point, coord, vecteur_repere_x)
                
                if point_rep.x < - demi_largeur:
                    points_gauche.append(point_rep)
                elif point_rep.x > demi_largeur:
                    points_droite.append(point_rep)
                else:
                    points_milieu.append(point_rep)

                if point_rep.y >= - voiture.longueur:
                    tous_y_derriere_vehicule = False

                if point_rep.y > un_y_devant_vehicule:
                    un_y_devant_vehicule = True

                if (vehicule_blocant is not None) and (point_rep.y < y_min_rep_blocage):
                    tous_y_devant_vehicule_blocant = False

            if not(un_y_devant_vehicule) or tous_y_derriere_vehicule or ((vehicule_blocant is not None) and tous_y_devant_vehicule_blocant):
                continue

            # si tous les points sont à droite ou à gauche : pas d'intersection

            if len(points_gauche) == 4 or len(points_droite) == 4:
                continue

            if points_milieu:
                # au moins 1 point au milieu
                point_y_min_milieu = min_liste_coord(points_milieu)

                if len(points_milieu) == 4:
                    cur_intersection = point_y_min_milieu
                else:

                    point_y_min_autour = min_liste_coord(points_gauche + points_droite)

                    if point_y_min_autour.x < -demi_largeur:
                        x_intersection = -demi_largeur
                    else:
                        x_intersection = demi_largeur

                    if point_y_min_milieu.y < point_y_min_autour.y:
                        # on a trouvé le point le plus proche
                        cur_intersection = point_y_min_milieu
                    else:
                        # on intersecte du bon côté la demi-droite
                        # entre point_y_min_milieu et point_y_min_autour
                        # droite y = a*x + b

                        a = (point_y_min_milieu.y - point_y_min_autour.y) / (point_y_min_milieu.x - point_y_min_autour.x)
                        b = point_y_min_milieu.y - (a * point_y_min_milieu.x)

                        y_intersection = (a * x_intersection) + b

                        cur_intersection = Coordonnees.Coordonnees(x_intersection, y_intersection)
            else:
                # pas de points au milieu
                point_y_min_gauche = min_liste_coord(points_gauche)
                point_y_min_droite = min_liste_coord(points_droite)

                if point_y_min_droite.y < point_y_min_gauche.y:
                    # on intersecte à droite
                    x_intersection = demi_largeur
                else:
                    # on intersecte à gauche
                    x_intersection = - demi_largeur

                a = (point_y_min_gauche.y - point_y_min_droite.y) / (point_y_min_gauche.x - point_y_min_droite.x)
                b = point_y_min_gauche.y - a * point_y_min_gauche.x

                y_intersection = a * x_intersection + b

                cur_intersection = Coordonnees.Coordonnees(x_intersection, y_intersection)

            if cur_intersection is not None:
                # on a trouvé une intersection

                if cur_intersection.y < 0:
                    continue

                # on prend l'intersection la plus proche

                cur_intersection_rep = Coordonnees.Coordonnees.inv_changer_repere(cur_intersection, coord, vecteur_repere_x)

                distance = abs(cur_intersection_rep - coord)

                if (distance < distance_blocage) or (vehicule_blocant is None):
                    vehicule_blocant = vehicule
                    distance_blocage = distance
                    coordonnees_blocage = cur_intersection_rep
                    y_min_rep_blocage = cur_intersection.y # y dans le repère local de la voiture

        if vehicule_blocant is not None:
            # on a bien une intersection

            bloque_par = vehicule_blocant.bloque_par

            if bloque_par is not None:
                if vehicule_blocant.timestamp_maj < voiture.timestamp_maj:
                    vehicule_blocant.bloque_par = None
                    bloque_par = vehicule_blocant
            else:
                bloque_par = vehicule_blocant

            if bloque_par != voiture:
                voiture.bloque_par = bloque_par
                return (coordonnees_blocage, vehicule_blocant)

        return (None, None)

    def notifie_temps(self, increment, moteur):
        #~ print("L'intersection a été notifié.")
        timestamp = moteur.temps / moteur.nombre_ticks_seconde
        config = self.gestionnaire.getConfig(timestamp, self.recuperer_etat_trafic(timestamp))
        self.appliquer_configuration(config, timestamp)
        

    def evaluer_situation(self):
        nb = 0

        for voie in (self.sortantes + self.entrantes):
            liste_vehicules = voie.get_vehicules()
        
            for vehicule in liste_vehicules:
                nb -= vehicule.time_alive

        liste_vehicules = self.vehicules

        for voiture in liste_vehicules:
            nb -= vehicule.time_alive

        return nb



    def recuperer_etat_trafic(self, timestamp):
        etat_trafic = {}
        etat_trafic["daytime"] = timestamp % (24 * 3600)
        i = 0
        for voie in (self.entrantes + self.sortantes):
            chaine = "occupation_voie_{0:d}".format(i)
            etat_trafic[chaine] = voie.nombre_vehicules()
            i += 1

        etat_trafic['occupation_intersection'] = len(self.vehicules)

        for identifiant, feu in self.feux.items():
            if feu.est_passant():
               etat = 1
            else:
               etat = 0
            
            duree_feu = feu.ticksRouge(timestamp)
            etat_trafic["etat_feu_{0}".format(identifiant)] = etat
            etat_trafic["dureestop_feu_{0}".format(identifiant)] = duree_feu

        return etat_trafic
