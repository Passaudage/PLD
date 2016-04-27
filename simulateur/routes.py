
import coordonnees
import controleAcces
import vehicule
	

class voie:
	def __init__(self, direction, controleur_acces, troncon, feu, coordonnees_debut, coordonnees_fin):
		self.intersectionsAccessibles = []
		self.controleur_acces = controleur_acces
		self.troncon = troncon
		self.coordonnees_debut = coordonnees_debut
		self.coordonnees_fin = coordonnees_fin
		self.vehicules = []
		self.directions = set()
		
		
		
	def creer_vehicule(discourtois, longueur):
		"""
			Crée le véhicule
			L'ajoute à la fin de la liste
			L'ajoute à l'arbre
		"""
		prochaine_direction = "droite";
		clio = vehicule(50, coordonnees_debut, discourtois, longueur, self, prochaine_direction, null)
		self.vehicules.append(clio)
		dernier_vehicule = self.vehicules[-1]
		clio.greffe_arbre(dernier_vehicule)
		
	def direction_possible(direction):
		return (direction in directions)


	def mise_a_jour_controle_acces(self, temps, simulation_manager):
		 self.controleur_acces.notifie_temps(self, temps, simulation_manager)

	def get_controleur_acces(self):
		return self.controleur_acces

	def puis_je_passer(self, direction):
		return

	#set de direction + probabilité de prendre cette direction en fonction des troncons accessibles et de leur proba

	#ajouter voiture

	#notification du véhicule en tête qui s'en va

	# dernier élément

	def setTroncon(self, troncon):
		self.troncon = troncon

class troncon:
	def __init__(self, tete, queue, probabilite_entree, longueur, coordonnees_):
		self.tete = tete
		self.queue = queue
		self.probabilite_entree = probabilite_entree
		self.longueur = longueur
		self.voies = []

	#trouver voie avec bonne direction
	def trouver_voie_direction(self, direction):
		voies_possibles = []
		for voie in self.voies:
			if(voie.direction_possible(direction)):
				voies_possibles.append(voie)
		return voies_possibles

	"""
	ainsi toujours poussé vers de nouveaux rivages
	dans la nuit éternelle emporté sans retour
	ne pourrons nous jamais sur l'océan des ages
	jetez l'ancre un seul jour ?
		AdL
	"""
