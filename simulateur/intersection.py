class intersection:
	
	def __init__(self, coordonnees, entrante, sortante, temps_vert=10, axe=0):
		"""
			# coordonees : Position de l'intersection sur la grille
			# entrante : voies entrantes selon le formalisme Bonfantien
			# sortante : voies sortantes selon le formalisme Bonfantien
			# temps_vert : temps que l'axe passé en parametre reste au vert en secondes
			# axe : 0 si axe 1-3, 1 si axe 2-4
			# /!\ Voir dessin Bonfante si questions /!\
		"""
		self.vehicules = []
		
		# Position de l'intersection
		self.coordonnees = coordonnees 
		
		# Liste voies entrantes
		# entrant[0] = voie tout droit et gauche
		# entrant[1] = voie tout droit et droite
		# /!\ Voir dessin Bonfante si questions /!\
		self.entrant = entrant 
		
		# Liste voies sortantes
		# sortant[0] = Droite 1
		# sortant[1] = Droite 2
		# sortant[2] = Tout droit 1
		# sortant[3] = Tout droit 2
		# sortant[4] = Gauche 1
		# sortant[5] = Gauche 2
		# /!\ Voir dessin Bonfante si questions /!\
		self.sortant = sortant 
		
		# Feu agissant sur l'intersection
		self.feu = feu(self,temps_vert,axe)
	
	def get_entrant(self):
		"""
			Retourne les voies entrantes
		"""
		return self.entrant
	
	def get_sortant(self):
		"""
			Retourne les voies sortantes
		"""
		return self.sortant
	
	def ajoute_vehicule(self,voiture):
		"""
			Ajoute une voiture au milieu du carrefour
		"""
		self.vehicules.append(voiture)
		
	def avancer_vehicule(self):
		"""
			Faire avancer les véhicules au milieu du carrefour
		"""
		for i in range(len(self.vehicules)):
			self.vehicules[i].avancer()
	
	def notifie_temps(self, temps, simulation_manager):
		"""
			Methode appelée lorsque le simulateur augmente le temps
		"""
		self.avancer_vehicule()