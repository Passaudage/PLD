import coordonnees


class vehicule:
	distance_minimale = 30 #cm
	self.vehicules_suivants = []
	self.simulateur
	proportion_discourtois = 0.8


	def __init__(self, max_acceleration, discourtois, coordonnees, longueur, voie, prochaine_direction, trajectoire, racine):
		self.coordonnees = coordonnees
		self.max_acceleration = max_acceleration
		self.longueur = longueur
		self.changeDirection(0,0)
		self.prochaine_direction = prochaine_direction
		self.vehicule_precedent
		self.racine = racine
		self.direction
		self.voie = voie
		self.intersection = None
		self.trajectoire = trajectoire
		voiture_fin = self.voie.get_dernier_element()
		self.greffe_arbre(voiture_fin)


	def changeDirection(self, x, y):
		self.direction = coordonnees(x, y)

	def avancerBoucle(pasTemporel):

		return False



	def calculerVitesse(self):
		return 1389*self.increment_temps #cm/increment_temps AIIIGHT


	def notifie_temps(self, nb_increment, simulateur):
		self.increment_temps = 1 / simulateur.nombre_ticks_seconde 
		self.avance_vehicule()
		if (len(self.vehicules_suivants) == 0):
			return
		else:
			for vehicule_suivant in self.vehicules_suivants:
				vehicule_suivant.notifie_temps


	def avance_vehicule(self):
		if(self.voie!=None):
			if(self.voie.direction_possible(self.prochaine_direction)):
				#tout droit
				if(self.vehicule_precedent.voie==self.voie):
					#on suit le véhicule devant
					self.suit_vehicule_devant()
				elif(self.vehicule_precedent.voie!=None):
					pass
					#on arrête de suivre le précédent de l'arbre (il est parti)
					self.decrochage()
					precedent = self.voie.precedent(self)
					if(precedent==None):
						if(self.verifie_feu()):
							#passer le feu
							pass
						else:
							self.avance_feu_rouge()
					else:
						self.greffe_arbre(precedent)
						self.suit_vehicule_devant() #on ne code avec le rectum par nos contrées
				else:
					if(self.verifie_feu()):
						#passer le feu
						pass
					else:
						self.avance_feu_rouge()
			else:
				pass
				#changer de voie, attention à la pile avant la voie
				if(self.vehicule_precedent.coordonnees==self.coordonnees):
					pass
					#pas encore dans le carrefour
				else:
					pass
					#changer de voie, demander bonne voie au tronçon, demander liste vehicules des voies d'à côté.
		elif(self.intersection!=None):
			pass
			#faire transition
		return
		
	def calculer_trajet_max(self, coordonnees_destination):
		distance_vecteur = coordonnees_destination.soustraction(self.coordonnees)
		distance_normee = distance_vecteur.norme()
		distance_possible = min (self.calculerVitesse() , distance_normee)
		trajet = self.trajectoire.mult(distance_possible)
		return trajet
		
	def suit_vehicule_devant(self):
		marge = self.trajectoire.mult(self.vehicule_precedent.longueur + distance_minimale) #longueur + distance minimale
		distance = self.vehicule_precedent.coordonnees.soustraction(marge)
		trajet = self.calculer_trajet_max(distance)
		self.coordonnees = self.coordonnees.addition(trajet)
		#on avance de ce que l'on peut
		
	def verifie_feu(self):
		return self.voie.est_passant(self.prochaine_direction)

	def avance_feu_rouge(self):
		trajet = self.calculer_trajet_max(self.voie.coordonnees_fin)
		self.coordonnees = self.coordonnees.addition(trajet)		

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

	def supp_vehicule_suivant(self,vehicule):
		self.vehicule_suivants.remove(vehicule)

	def decrochage(self):
		self.vehicule_precedent.supp_vehicule_suivant(self)
		self.vehicule_precedent = None
		self.propager_racine(self)

	def propager_racine(self,racine):
		self.racine = racine
		if(len(self.vehicules_suivants)!=0):
			for vehicule_suivant in self.vehicules_suivants:
				vehicule_suivant.propager_racine(racine)


		#suis je sur la bonne direction ?

		#Quel monde cruel aije mis au monde ?
