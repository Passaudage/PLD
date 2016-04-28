import Coordonnees
from Voie import *
from Troncon import *
import Intersection


class Vehicule:
	distance_minimale = 30 #cm
	proportion_discourtois = 0.8


	def __init__(self, simulateur, max_acceleration, discourtois, coordonnees, longueur, voie, prochaine_direction, origine, destination, direction, vehicule_precedent):
		self.coordonnees = coordonnees
		self.max_acceleration = max_acceleration
		self.longueur = longueur
		self.prochaine_direction = prochaine_direction
		self.voie = voie
		self.origine = 
		self.destination = destination
		self.orientation_cible = direction	
		self.direction = direction
		self.vitesse = (0,0)
		
		#non initialisés
		self.racine = None
		self.nouvelle_voie = None
		self.intersection = None
		
		#Mise dans l'arbre
		self.vehicule_precedent = vehicule_precedent
		self.vehicules_suivants = []
		if(vehicule_precedent!=None):
			self.greffe_arbre(vehicule_precedent)
		else:
			self.racine = self
			#se déclarer tête de liste

	def changeDirection(self, x, y):
		self.direction = Coordonnees(x, y)

	def avancerBoucle(pasTemporel):

		return False


	def calculerVitesse(self):
		return 1389*self.increment_temps #cm/increment_temps AIIIGHT


	def notifie_temps(self, nb_increment, simulateur):
		self.avance_vehicule(nb_increment, simulateur.nombre_ticks_seconde)
		if (len(self.vehicules_suivants) == 0):
			return
		else:
			for vehicule_suivant in self.vehicules_suivants:
				vehicule_suivant.notifie_temps
				
	def mettre_coordonnees_a_jour(incr,nb,vit,pos):
		return


	def avance_vehicule(self, incr, nb_tick):
		#si on existe pas encore
		if(self.vehicule_precedent.coordonnees==self.coordonnees): 
			return
					
		#si on est sur une voie
		if(self.intersection==None):
			
			#si on est sur une bonne voie
			if(self.voie.direction_possible(self.prochaine_direction)):
				
				#si le véhicule précédent dans l'arbre est bien devant 
				if(self.vehicule_precedent.voie==self.voie):
					
					arriere_vehicule = (self.vehicule_precedent.coordonnees - self.direction*longueur)
					self.mettre_coordonnees_a_jour(incr, nb_tick, self.vehicule_precedent.vitesse, arriere_vehicule) 
					
				#sinon si le précédent a changé de voie au sein du même troncon
				elif(self.vehicule_precedent.voie.troncon == self.voie.troncon):
					
					#on arrête de suivre le précédent de l'arbre (il est parti)
					self.decrochage_arbre()
					precedent = self.voie.precedent(self)
					
					#si il y a encore quelqu'un devant, sur la voie
					if(precedent!=None):
						
						self.greffe_arbre(precedent)
						arriere_vehicule = (self.vehicule_precedent.coordonnees - self.direction*longueur)
						self.mettre_coordonnees_a_jour(incr, nb_tick, self.vehicule_precedent.vitesse, arriere_vehicule)  
						#on ne code avec le rectum par nos contrées
									
					#si on est le premier sur la voie
					else:
						
						#si le feu est vert
						if(self.verifie_feu()):
							
							#passer le feu
							pass
						
						#sinon
						else:
							
							self.mettre_coordonnees_a_jour(incr, nb_tick, (0,0), self.destination) 
				
				#si le précédent a passé l'intersection et que l'on a dépassé le feu
				elif ((coordonnees-destination)*direction >= 0):
					
					self.origine = self.coordonnees
					self.intersection = self.voie.demander_intersection()
					self.intersection.ajouter_vehicule(self)
					self.voie.supprimer_vehicule(self)
					
					self.nouvelle_voie = self.intersection.demander_voies_sorties(self.voie, self.prochaine_direction)
					self.destination = self.nouvelle_voie.coordonnees_debut
					self.orientation_cible = self.nouvelle_voie.orientation
					
					
					
					self.mettre_coordonnees_a_jour(incr, nb_tick, 
				
				#si le précédent a passé l'intersection et que l'on est encore sur la voie
				else:
					
					distance_faite = self.avance_feu()
					
					#si le feu est vert
					if(self.verifie_feu()):
					
					#si le feu est rouge
					else:
						
						pass #on bouge pas
			
			#si on est sur une mauvaise voie
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
						
				#si on est arrivé sur la bonne voie
				if(self.coordonnees == self.destination) :#changement de voie termine
					
					self.voie = self.nouvelle_voie
					self.nouvelle_voie = None
					self.destination = self.voie.coordonnees_fin
					self.direction = self.voie.direction
					self.voie.insertion_dans_liste(self,self.vehicule_precedent)
						
		#si on est sur l'intersection		
		elif(self.intersection!=None):
			
			pass
			#faire transition
			
		return
		
	def calculer_trajet_max(self, coordonnees_destination):
		distance_vecteur = coordonnees_destination.soustraction(self.coordonnees)
		distance_normee = distance_vecteur.norme()
		distance_possible = min (self.calculerVitesse() , distance_normee)
		trajet = self.direction.mult(distance_possible)
		resultat = self.coordonnees.addition(trajet)
		return resultat
		
	def suit_vehicule_devant(self):
		marge = self.direction.mult(self.vehicule_precedent.longueur + distance_minimale) #longueur + distance minimale
		distance = self.vehicule_precedent.coordonnees.soustraction(marge)
		resultat = self.calculer_trajet_max(distance)
		self.coordonnees = resultat
		#on avance de ce que l'on peut
		
	def verifie_feu(self):
		return self.voie.est_passant(self.prochaine_direction)

	def avance_feu(self):
		resultat = self.calculer_trajet_max(self.voie.coordonnees_fin)
		distance_faite = abs(resultat - self.coordonnees)
		self.coordonnees = resultat
		return distance_faite
		
	def avance_change_voie(self):
		trajet = self.calculer_trajet_max(self.destination.soustraction(self.direction.mult(30)))
		self.coordonnees = self.coordonnees.addition(trajet)

	def avancer_intersection(self, distance_faite):
		trajet = self.calculer_trajet_max(self.destination)
		

	#S'ajouter en feuille sur un arbre
	def greffe_arbre(self,vehicule_precedent):
		if(vehicule_precedent.racine == self.racine):
			return
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
				
	def donner_arriere(self):
		return (self.coordonnees - self.direction*longueur)


		#suis je sur la bonne direction ?

		#Quel monde cruel ai-je mis au monde ?
