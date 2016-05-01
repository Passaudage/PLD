import Feu
import Coordonnees
import Vehicule
import time

"""
    Si tu vois une chevre dans le repaire d'un lion, aie peur d'elle.
"""

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
    vitesse_max = 972 # cm.s^{-1}
    sur_place = {}
        
    def __init__(self, coordonnees, hauteur, largeur):
        # Position du point central de l'intersection
        self.coordonnees = coordonnees
        self.hauteur = hauteur
        self.largeur = largeur
        
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
                    feu = Feu.Feu(self)
                    self.feux[index] = feu
                # On ajoute le feu a ce troncon
                troncon.ajouter_feux(sens,direction, feu)

                
    def construire_chemins(self): #TODO : A corriger
        if (self.troncon_gauche == None or self.troncon_droite == None or self.troncon_haut == None or self.troncon_bas == None):
            raise Exception("Tous les troncons ne sont pas initialisés")
        else:
            liste_troncon = self.lister_troncon()
            for troncon in liste_troncon :
                alignement = troncon.coordonnees_debut - self.coordonnees
                if (alignement.x != 0 and alignement.y != 0):
                    raise Exception("Le troncon " + troncon + " n'est pas aligné correctement, il est bancale : " + str(troncon.coordonnees_debut.x) + " " + str(troncon.coordonnees_debut.y))

                demi_largeur = troncon.largeur()/2
                
                point_tr_gauche = troncon.coordonnees_debut - Coordonnees.Coordonnees(demi_largeur,demi_largeur)
                point_tr_droite = troncon.coordonnees_debut + Coordonnees.Coordonnees(demi_largeur,demi_largeur)
                adj1 = liste_troncon[liste_troncon.index(troncon)-1]
                adj2 = liste_troncon[liste_troncon.index(troncon)-1]
                alignement1 = point_tr_gauche - adj1.coordonnees_debut
                alignement2 = point_tr_droite- adj1.coordonnees_debut
                
                print(troncon)
                print(alignement1)
                print(alignement2)
                print()
                
                #~ co1 =None
                #~ if(liste_troncon.index(troncon)+1==len(liste_troncon)):
                    #~ co1= liste_troncon[0].coordonnees_debut
                #~ else: co1 = liste_troncon[liste_troncon.index(troncon)+1].coordonnees_debut
                #~ co2 = liste_troncon[liste_troncon.index(troncon)-1].coordonnees_fin
                #~ alignement1 = troncon.coordonnees_debut - co1 + Coordonnees.Coordonnees(demi_largeur, demi_largeur)
                #~ alignement2 = troncon.coordonnees_debut - co2 + Coordonnees.Coordonnees(demi_largeur, demi_largeur)
                #~ alignement3 = troncon.coordonnees_debut - co1 - Coordonnees.Coordonnees(demi_largeur, demi_largeur)
                #~ alignement4 = troncon.coordonnees_debut - co2 - Coordonnees.Coordonnees(demi_largeur, demi_largeur)
                #~ print(alignement1.x)
                #~ print(alignement2.x)
                #~ print(alignement3.x)
                #~ print(alignement4.x)
                #~ print(alignement1.y)
                #~ print(alignement2.y)
                #~ print(alignement3.y)
                #~ print(alignement4.y)
                #~ if(alignement1.x != 0 and alignement1.y != 0 and alignement3.x != 0 and alignement3.y != 0):
                    #~ raise Exception("Le troncon n'est pas ajusté correctement à gauche : " + str(troncon.coordonnees_debut.x) + " " + str(troncon.coordonnees_debut.y))
                #~ if(alignement2.x != 0 and alignement2.y != 0 and alignement4.x != 0 and alignement4.y != 0):
                    #~ raise Exception("Le troncon n'est pas ajusté correctement à droite : " + str(troncon.coordonnees_debut.x) + " " + str(troncon.coordonnees_debut.y))

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
        print("-> Voiture référence : " + str(voiture))
        print("   pos : " + str(coord))
        print("   dir : " + str(direction))

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

                print(point_rep)

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

        return (coordonnees_blocage, vehicule_blocant)

    def notifie_temps(self, increment, moteur):
        #~ print("L'intersection a été notifié.")
        pass
