from enum import Enum
class Couleur(Enum):
	"""
		Enumération utilisée pour la couleur des feux
	"""
	rouge = 0
	vert = 1

class feu(controleAcces):
		"""
			Modélise un feu de signalisation.
				# intersection : Intersection sur laquelle agit le feu
				# temps_vert : temps durant lequel l'axe passé en parametre reste vert en secondes
				# temps_cycle : temps du cycle en secondes
				# @author : Bonfante
		"""
	
	def __init__(self, intersection, temps_vert=10, temps_cycle = 20):
		# Intersection ou se trouve le feu
		self.intersection = intersection
		
		# Temps que l'axe passé en parametre reste vert
		self.temps_vert = temps_vert
		
		# Temps de la durée d'un cycle de feu
		self.temps_cycle = temps_cycle
		
		# Couleur actuel de l'axe passé en parametre
		self.couleur_axe = Couleur.vert

	def notifie_temps(self, temps, simulation_manager):
		"""
			Methode appelée lorsque le simulateur augmente le temps
		"""
		self.change_couleur(temps, simulation_manger)
		
	def change_couleur(self,temps, simulation_manger):
		"""
			Change la couleur du feu en fonction du temps
		"""
		# Recupere le temps absolu dans le simulation manager
		temps_absolu = simulation_manager.get_temps_absolu()
		# Choisir la bonne couleur du feu
		temp = temps_absolu%self.temps_cycle
		if(temp<self.temps_vert):
			self.couleur_axe = Couleur.vert
		else:
			self.couleur_axe = Couleur.rouge
	
	def est_passant(self):
		return self.couleur_axe == Couleur.vert