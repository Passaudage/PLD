import Feu
import Coordonnees
"""
    Si tu vois une chevre dans le repaire d'un lion, aie peur d'elle.
"""

class Intersection:
    """
        Modelise une intersection.
            # coordonees : Position de l'intersection sur la grille
            # @author : Bonfante
    """
    vitesse_max = 972 # cm.s^{-1}
        
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
        self._creer_feux_troncon(1, self.troncon_bas, self.troncon_bas.voies_sens1, 3)
        self._creer_feux_troncon(2, self.troncon_haut, self.troncon_haut.voies_sens2, 1)
        self._creer_feux_troncon(1, self.troncon_gauche, self.troncon_gauche.voies_sens1, 2)
        self._creer_feux_troncon(2, self.troncon_droite, self.troncon_droite.voies_sens2, 0)

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
            feu = None
            for direction in voie.directions:
                # On choisit le bon feu
                if(direction == 'D'):
                    index = 2+3*offset
                elif(direction == 'G'):
                    index = 0+3*offset
                elif(direction == 'TD'):
                    index = 1+3*offset
                # Si le feu existe 
                if(index in self.feux.keys()):
                    feu = self.feux[index]
                # Si le feu n'existe pas
                else:
                    feu = Feu.Feu(self,direction)
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

    def donner_obstacle(self, coord, direction):
        coordonnees_blocage = None
        distance_blocage = 0
        vehicule_blocant = None

        for vehicule in self.vehicules :
            cur_pos = vehicule.coordonnees # position du nez de la voiture
            cur_dir = vehicule.direction # orientation de la voiture
            cur_long = vehicule.longueur

            cur_intersection = None
            sens_opposes = None

            gamma = None
            mu = None

            # colinéaires ?

            if abs(direction * cur_dir) == 1: # TODO prendre en compte un epsilon
                # trajectoires colinéaires

                if direction.x != 0:
                    mu = (cur_pos.x - coord.x) / direction.x

                    if cur_pos.y == (coord.y + mu * direction.y):
                        # support confondu
                        sens_opposes = (abs(direction * cur_dir) / (direction * cur_dir)) < 0

                    # sinon trajectoires strictement parallèles

                else:
                    # direction est normé, donc on est certain que (direction.y != 0)
                    mu = (cur_pos.y - coord.y) / direction.y

                    if cur_pos.x == (coord.x + mu * direction.x):
                        # support confondu
                        sens_opposes = (abs(direction * cur_dir) / (direction * cur_dir)) < 0
                    # sinon trajectoires strictement parallèles

                if sens_opposes is not None:

                    if sens_opposes:
                        # en sens opposés : de nez à nez
                        cur_intersection = cur_pos
                    else:
                        # de nez à dos (on enlève la longueur de la voiture de devant)
                        cur_intersection = cur_pos - cur_dir * cur_long

            else:
                # trajectoires non colinéaires
                if direction.x != 0:
                    ratio = direction.y / direction.x
                    gamma = (coord.x + ratio * (cur_pos.y - coord.y) - cur_pos.x) / (cur_dir.x - ratio * cur_dir.y)
                    mu = (cur_pos.y + gamma * cur_dir.y - coord.y) / direction.y
                else:
                    # direction est normé, donc on est certain que (direction.y != 0)
                    ratio = direction.x / direction.y
                    gamma = (coord.y + ratio * (cur_pos.x - coord.x) - cur_pos.y) / (cur_dir.y - ratio * cur_dir.x)
                    mu = (cur_pos.x + gamma * cur_dir.x - coord.x) / direction.x

                if (gamma > 0 and gamma < vehicule.longueur) and (mu > 0):
                    cur_intersection = coord + direction * mu

            if cur_intersection is not None:
                # on a trouvé une intersection
                # on prend l'intersection la plus proche

                distance = abs(cur_intersection - coord)

                if (vehicule_blocant is None) or (distance < distance_blocage):
                    vehicule_blocant = vehicule
                    distance_blocage = distance
                    coordonnees_blocage = cur_intersection


        return (coordonnees_blocage, vehicule_blocant)

    def notifie_temps(self, increment, moteur):
        #~ print("L'intersection a été notifié.")
        pass
