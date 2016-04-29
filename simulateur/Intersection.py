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
            
            # Cree les feux et les donne aux troncons
            self.creer_feux(1,troncon, self.entrantes, 2)

            
        elif(position=='B'):
            if(self.troncon_bas != None):
                raise Exception("Troncon deja ajoute en bas.")
            # Ajoute les voies entrantes et sortantes
            self.entrantes += troncon.voies_sens1
            self.sortantes += troncon.voies_sens2
            
            # Ajoute le troncon
            self.troncon_bas = troncon
            
            # Cree les feux et les donne aux troncons
            self.creer_feux(1,troncon, self.entrantes, 3)
            
        elif(position=='D'):
            if(self.troncon_droite != None):
                raise Exception("Troncon deja ajoute a droite.")
            # Ajoute les voies entrantes et sortantes
            self.entrantes += troncon.voies_sens2
            self.sortantes += troncon.voies_sens1
            
            # Ajoute le troncon
            self.troncon_droite = troncon
            
            # Cree les feux et les donne aux troncons
            self.creer_feux(2,troncon, self.entrantes, 0)
            
        elif(position=='H'):
            if(self.troncon_haut != None):
                raise Exception("Troncon deja ajoute en haut.")
            # Ajoute les voies entrantes et sortantes
            self.entrantes += troncon.voies_sens2
            self.sortantes += troncon.voies_sens1
            
            # Ajoute le troncon
            self.troncon_haut = troncon
            
            # Cree les feux et les donne aux troncons
            self.creer_feux(2, troncon, self.entrantes, 1)
            
        else:
            raise Exception(position+" n'est pas une direction convenable.")
    
    def creer_feux(self, sens, troncon, voies_entrantes, offset):
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

    def donner_obstacle(self, coordonnees, direction):
        coordonnee_blocage = None
        dist = 0
        vehicule_blocant = None
        a = direction.y / direction.x
        b = coordonnees.y - a*coordonnees.x

        #vrai si direction va vers la droite
        droite = Coordonnees.Coordonnees(1,0)*direction > 0

        for vehicule in self.vehicules :
            ar = vehicule.donner_arriere()
            av = vehicule.coordonnees
            a2 = (av.y-ar.y) / (av.x-ar.x)
            b2 = av.y - a*av.x
            x = (b - b2) / (a2 - a)
            if (((droite and direction.x<=x)or(not droite and x<=direction.x)) and ((av.x<=x and x<=ar.x) or (ar.x<=x and x<=av.x))):
                nouvelle_co = Coordonnees.Coordonnees(x,a*x+b)
                if (coordonnee_blocage == None or dist > abs(nouvelle_co-coordonnees)):
                    vehicule_blocant = vehicule
                    coordonnee_blocage = nouvelle_co
                    dist = abs(nouvelle_co-coordonnees)

        return (coordonnee_blocage,vehicule_blocant)

    def notifie_temps(self, increment, moteur):
        #~ print("L'intersection a été notifié.")
        pass
