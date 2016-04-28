"""
    Si tu vois une chevre dans le repaire d'un lion, aie peur d'elle.
"""

class Intersection:
    """
        Modelise une intersection.
            # coordonees : Position de l'intersection sur la grille
            # @author : Bonfante
    """
        
    def __init__(self, coordonnees):
        # Position du point central de l'intersection
        self.coordonees = coordonees
        
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
        self.sortantes = {}
        
        # Chemins voitures
        # Map voiture/Liste de points restant à passer
        self.chemins_voitures = {}
        
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
            
            # Cree les feux et les donne aux voies
            self.creer_feux(voies_entrantes, 2)
            
        elif(position=='B'):
            if(self.troncon_bas != None):
                raise Exception("Troncon deja ajoute en bas.")
            # Ajoute les voies entrantes et sortantes
            self.entrantes += troncon.voies_sens1
            self.sortantes += troncon.voies_sens2
            
            # Ajoute le troncon
            self.troncon_bas = troncon
            
            # Cree les feux et les donne aux voies
            self.creer_feux(voies_entrantes, 3)
            
        elif(position=='D'):
            if(self.troncon_droite != None):
                raise Exception("Troncon deja ajoute a droite.")
            # Ajoute les voies entrantes et sortantes
            self.entrantes += troncon.voies_sens2
            self.sortantes += troncon.voies_sens1
            
            # Ajoute le troncon
            self.troncon_droite = troncon
            
            # Cree les feux et les donne aux voies
            self.creer_feux(voies_entrantes, 0)
            
        elif(position=='H'):
            if(self.troncon_haut != None):
                raise Exception("Troncon deja ajoute en haut.")
            # Ajoute les voies entrantes et sortantes
            self.entrantes += troncon.voies_sens2
            self.sortantes += troncon.voies_sens1
            
            # Ajoute le troncon
            self.troncon_haut = troncon
            
            # Cree les feux et les donne aux voies
            self.creer_feux(voies_entrantes, 1)
            
        else:
            raise Exception(position+" n'est pas une direction convenable.")
    
    def creer_feux(voies_entrantes, offset):
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
                    feu = Feu(self,direction)
                    self.feux[index] = feu
                # On ajoute le feu a cette voie
                voie.ajoute_feu(feu)
                
	def trouve_voies_sorties(self,voie_entree,direction):
		"""
			Trouve les voies de sorties possibles si l'on
			arrive sur la voie voie_entree en direction de 
			la direction passe en parametre
				# voie_entree : voie d'origine
				# direction : la direction ou l'on va
				# @author : Bonfante
		"""
		# Si la voie est dans le troncon gauche
		voies = troncon_gauche.voies_sens1
		for voie in voies:
			if(voie == voie_entree):
				if(direction == 'D'):
					return troncon_bas.voies_sens2
				elif(direction == 'G'):
					return troncon_haut.voies_sens1
				elif(direction == 'TD'):
					return troncon_droite.voies_sens1
				
		# Si la voie est dans le troncon droit
		voies = troncon_gauche.voies_sens2
		for voie in voies:
			if(voie == voie_entree):
				if(direction == 'D'):
					return troncon_haut.voies_sens1
				elif(direction == 'G'):
					return troncon_bas.voies_sens2
				elif(direction == 'TD'):
					return troncon_gauche.voies_sens2
		
		# Si la voie est dans le troncon haut
		voies = troncon_gauche.voies_sens2
		for voie in voies:
			if(voie == voie_entree):
				if(direction == 'D'):
					return troncon_gauche.voies_sens2
				elif(direction == 'G'):
					return troncon_droite.voies_sens1
				elif(direction == 'TD'):
					return troncon_bas.voies_sens2
		# Si la voie est dans le troncon bas
		voies = troncon_gauche.voies_sens1
		for voie in voies:
			if(voie == voie_entree):
				if(direction == 'D'):
					return troncon_droite.voies_sens1
				elif(direction == 'G'):
					return troncon_gauche.voies_sens2
				elif(direction == 'TD'):
					return troncon_haut.voies_sens1
				