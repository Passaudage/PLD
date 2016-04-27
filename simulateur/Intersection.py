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
		# Liste des voitures sur l'intersection
		self.vehicules = []
		
		# Position de l'intersection
		self.coordonnees = coordonnees 
		
		# Liste voies entrantes
		self.entrant = [] 
		
		# Liste voies sortantes
		self.sortant = [] 
		
		# Liste controleurs d'acces (feux)
		self.controleurs_acces = []
			
	def ajoute_voie_entree(self, voie):
		"""
			Ajoute une voie entrante sur l'intersection 
			avec le controleur d'acces associe
		"""
		self.entrant.append(voie)
		self.controleurs_acces.append(voie.controleur_acces)
		
	def ajoute_voie_sortie(self,voie):
		"""
			Ajoute une voie sortante sur l'intersection 
		"""
		self.sortant.append(voie)
		
	def ajoute_vehicule(self,voiture): ## TODO Utile ??
		"""
			Ajoute une voiture au milieu du carrefour
		"""
		self.vehicules.append(voiture)
		
	def notifie_temps(self, temps, simulation_manager):
		"""
			Methode appelee lorsque le simulateur augmente le temps
		"""
		self.mise_a_jour_controle_acces(temps,simulation_manager)
		self.avancer_vehicule()
		
	def avancer_vehicule(self):
		"""
			Faire avancer les vehicules au milieu du carrefour
		"""
		for i in range(len(self.vehicules)):
			self.vehicules[i].avancer()
			
	def mise_a_jour_controle_acces(self, temps, simulation_manager):
		"""
			Mise a jour des controleurs d'acces
		"""
		for i in range(len(self.controleurs_acces)):
			self.controleurs_acces[i].notifie_temps(temps, simulation_manager) 
	
