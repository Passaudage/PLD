import coordonnees


class vehicule:
	self.vehicules_suivants = []
	self.simulateur
	proportion_discourtois = 0.8


	def __init__(self, max_acceleration, discourtois, coordonnees, longueur, voie, prochaine_direction, racine):
		self.coordonnees = coordonnees
		self.max_acceleration = max_acceleration
		self.longueur = longueur
		self.changeDirection(0,0)
		self.prochaine_direction = prochaine_direction
		self.vehicule_precedent
		self.racine = racine
		self.direction
		self.voie = voie
		self.intersection = null

		voiture_fin = self.voie.get_dernier_element()
		self.greffe_arbre(voiture_fin)


	def changeDirection(self, x, y):
		self.direction = coordonnees(x, y)

	def avancerBoucle(pasTemporel):

		return False



	def calculerVitesse(self):

		return


	def notifie_temps(self):
		self.avance_vehicule
		if (len(self.vehicules_suivants) == 0):
			return
		else:
			for vehicule_suivant in self.vehicules_suivants:
				vehicule_suivant.notifie_temps


	def avance_vehicule(self):
		if(self.voie!=null):
			if(self.voie.direction_possible(self.prochaine_direction)):
				#tout droit
				if(self.vehicule_precedent.voie==self.voie):
					pass
			else:
				pass
				#changer de voie, attention à la pile avant la voie
		elif(self.intersection!=null):
			pass
			#faire transition
		return


	#S'ajouter en feuille sur un arbre
	def greffe_arbre(self,vehicule_precedent):
		self.set_vehicule_precedent(vehicule_precedent)
		vehicule_precedent.set_vehicules_suivants(self)


	def set_vehicule_precedent(self, vehicule):
		self.vehicule_precedent = vehicule


	def set_vehicules_suivants(self, vehicules):
		self.vehicules_suivants = vehicules

	def add_vehicule_suivant(self,vehicule):
		self.vehicules_suivants.append(vehicule)


	def propager_racine(self,racine):
		self.racine = racine
		if(len(self.vehicules_suivants)!=0):
			for vehicule_suivant in self.vehicules_suivants:
				vehicule_suivant.propager_racine(racine)


		#suis je sur la bonne direction ?

		#Quel monde cruel aije mis au monde ?
