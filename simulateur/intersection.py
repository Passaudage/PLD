class intersection:
		"""
			Modélise une intersection.
				# coordonees : Position de l'intersection sur la grille
				# @author : Bonfante
		"""
	
	def __init__(self, coordonnees):
		# Liste des voitures sur l'intersection
		self.vehicules = []
		
		# Position de l'intersection
		self.coordonnees = coordonnees 
		
		# Liste voies entrantes
		self.entrant = [] 
		
		# Liste voies sortantes
		self.sortant = [] 
			
	def ajoute_voie_entree(self, voie):
		"""
			Ajoute une voie entrante sur l'intersection 
			avec le controleur d'acces associé
		"""
		self.entrant.append(voie)
		
	def ajoute_voie_sortie(self,voie):
		"""
			Ajoute une voie sortante sur l'intersection 
		"""
		self.sortant.append(voie)
		
	def ajoute_controle_acces(self,controle_acces):
		self.controle_acces.append(controle_acces)
	
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
			
	def mise_a_jour_controle_acces(self, temps, simulation_manager):
		"""
			Mise à jour des controleurs d'acces
		"""
		for i in range(len(self.entrant)):
			self.entrant[i].mise_a_jour_controle_acces(temps, simulation_manager)
	
	def notifie_temps(self, temps, simulation_manager):
		"""
			Methode appelée lorsque le simulateur augmente le temps
		"""
		self.mise_a_jour_controle_acces(temps,simulation_manager)
		self.avancer_vehicule()