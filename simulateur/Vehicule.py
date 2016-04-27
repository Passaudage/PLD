import coordonnees
from routes import *
import intersection


class Vehicule:
	distance_minimale = 30 #cm
	proportion_discourtois = 0.8


	def __init__(self, simulateur, max_acceleration, discourtois, coordonnees, longueur, voie, prochaine_direction, direction, vehicule_precedent):
		self.coordonnees = coordonnees
		self.max_acceleration = max_acceleration
		self.longueur = longueur
		self.prochaine_direction = prochaine_direction
		self.voie = voie
		self.destination = self.voie.coordonnees_fin		
		self.direction = direction
		self.simulateur = simulateur
		
		#non initialisés
		self.racine = None
		self.nouvelle_voie = None
		self.intersection = None
		
		#Mise dans l'arbre
		self.vehicule_precedent
		self.vehicules_suivants = []
		if(vehicule_precedent!=self):
			self.greffe_arbre(voiture_fin)
		else
			self.racine = self
			#se déclarer tête de liste
			
			
		
		


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
					self.decrochage_arbre()
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
						#passer le feu, demander l'intersection, demander direction
						pass
					else:
						self.avance_feu_rouge()
			else:
				if(self.vehicule_precedent.coordonnees==self.coordonnees):
					pass
					#pas encore dans le carrefour
				else:
					#changer de voie, demander bonne voie au tronçon, demander liste vehicules des voies d'à côté.
					self.nouvelle_voie = self.voie.troncon.trouver_voie_direction(prochaine_direction)[0]
					direction_virage = self.nouvelle_voie.coordonnees_debut.soustraction(self.voie.coordonnees_debut)
					distance_avant = self.direction.mult(2)
					direction_non_normalisee = direction_virage.addition(distance_avant)
					self.destination = direction_non_normalisee + self.coordonnees
					self.direction = direction_non_normalisee.normaliser()
					
					for vehicule in self.voie.vehicules:
						if((vehicule.coordonnees - vehicule.voie.direction.mult(vehicule.longueur) - vehicule.voie.coordonnees_debut).norme() < (self.coordonnees.addition(self.direction).soustraction(vehicule.voie.coordonnees_debut)).norme()): #direction dans voie
							pass
						elif((vehicule.coordonnees - vehicule.voie.coordonnees_debut).norme() > (self.coordonnees.addition(self.direction).soustraction(vehicule.voie.coordonnees_debut)).norme()): #direction dans voie
							self.decrochage_arbre()
							self.greffe_arbre(vehicule)
							self.avance_change_voie()
						else: 
							self.decrochage_arbre()
							self.avance_change_voie()
							self.greffe_arbre(vehicule.vehicule_precedent)
					if(self.coordonnees == self.destination) :#changement de voie termine
						self.voie = self.nouvelle_voie
						self.nouvelle_voie = None
						self.destination = self.voie.coordonnees_fin
						self.direction = self.voie.direction
						self.voie.insertion_dans_liste(self,self.vehicule_precedent)
						
				
		elif(self.intersection!=None):
			pass
			#faire transition
		return
		
	def calculer_trajet_max(self, coordonnees_destination):
		distance_vecteur = coordonnees_destination.soustraction(self.coordonnees)
		distance_normee = distance_vecteur.norme()
		distance_possible = min (self.calculerVitesse() , distance_normee)
		trajet = self.direction.mult(distance_possible)
		return trajet
		
	def suit_vehicule_devant(self):
		marge = self.direction.mult(self.vehicule_precedent.longueur + distance_minimale) #longueur + distance minimale
		distance = self.vehicule_precedent.coordonnees.soustraction(marge)
		trajet = self.calculer_trajet_max(distance)
		self.coordonnees = self.coordonnees.addition(trajet)
		#on avance de ce que l'on peut
		
	def verifie_feu(self):
		return self.voie.est_passant(self.prochaine_direction)

	def avance_feu_rouge(self):
		trajet = self.calculer_trajet_max(self.voie.coordonnees_fin)
		self.coordonnees = self.coordonnees.addition(trajet)		
		
	def avance_change_voie(self):
		trajet = self.calculer_trajet_max(self.destination.soustraction(self.direction.mult(30)))
		self.coordonnees = self.coordonnees.addition(trajet)


	#S'ajouter en feuille sur un arbre
	def greffe_arbre(self,vehicule_precedent):
		self.set_vehicule_precedent(vehicule_precedent)
		vehicule_precedent.set_vehicules_suivants(self)
		self.propager_racine(vehicule_precedent.racine)
		
	def change_arbre(self,vehicule_precedent):
		self.vehicule_precedent.supp_vehicule_suivant(self)
		self.set_vehicule_precedent(vehicule_precedent)
		vehicule_precedent.set_vehicules_suivants(self)
		self.propager_racine(vehicule_precedent.racine)


	def set_vehicule_precedent(self, vehicule):
		self.vehicule_precedent = vehicule


	def set_vehicules_suivants(self, vehicules):
		self.vehicules_suivants = vehicules

	def add_vehicule_suivant(self,vehicule):
		self.vehicules_suivants.append(vehicule)

	def supp_vehicule_suivant(self,vehicule):
		self.vehicule_suivants.remove(vehicule)

	def decrochage_arbre(self):
		self.vehicule_precedent.supp_vehicule_suivant(self)
		self.vehicule_precedent = None
		self.propager_racine(self)

	def propager_racine(self,racine):
		self.racine = racine
		if(len(self.vehicules_suivants)!=0):
			for vehicule_suivant in self.vehicules_suivants:
				vehicule_suivant.propager_racine(racine)


		#suis je sur la bonne direction ?

		#Quel monde cruel ai-je mis au monde ?
