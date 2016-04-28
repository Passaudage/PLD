from Coordonnees import *
from Voie import *
from Troncon import *
import Intersection
import random


class Vehicule:
        distance_minimale_roulant = 150 #cm
	distance_minimale = 30 #cm
	proportion_discourtois = 0.8
        acceleration_max = 100 # cm.s^(-2)

	def __init__(self, simulateur, max_acceleration, discourtois, coordonnees, longueur, voie, prochaine_direction, destination, direction, vehicule_precedent):
		self.coordonnees = coordonnees
		self.max_acceleration = max_acceleration
		self.longueur = longueur
		self.prochaine_direction = prochaine_direction
		self.voie = voie
		self.destination = destination	
		self.direction = direction
		self.simulateur = simulateur
                self.vitesse = Coordonnees()
                self.acceleration = Coordonnees()
                self.politesse_changement_voie = random.random()
		
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
		self.increment_temps = nb_increment / (simulateur.nombre_ticks_seconde)
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
				if(self.vehicule_precedent.voie == self.voie):
					#on suit le véhicule devant
					self.suit_vehicule_devant()
				elif(self.vehicule_precedent.voie!=None):
					#on arrête de suivre le précédent de l'arbre (il est parti)
					self.decrochage_arbre()
					precedent = self.voie.precedent(self)
					if(precedent==None):
						if(self.verifie_feu()):
							#passer le feu
							pass
						else:
							self.avance_feu()
					else:
						self.greffe_arbre(precedent)
						self.suit_vehicule_devant()
				else:
					distance_faite = self.avance_feu()
					if(self.verifie_feu()):
						#passer le feu, demander l'intersection, demander direction
						if(self.coordonnees == self.voie.coordonnees_fin):
							self.intersection = self.voie.demander_intersection()
							self.intersection.ajouter_vehicule(self)
							self.destination = self.intersection.demander_voies_sorties(self.voie, self.prochaine_direction, self.coordonnees)
							self.direction = (self.destination-self.coordonnees).normaliser()
							#nouvelle destination et direction données par l'intersection
							self.avancer_intersection(distance_faite)
					else:
						pass
						#feu rouge, on bouge pas
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
		
        def mettre_coordonees_a_jour(increment_temps, nb_ticks_sec, vitesse_precedent, position):
            if self.intersection != None:
                print('not implemented')
            else:
                dx = self.vitesse.x * increment_temps / nb_ticks_sec 
                dy = self.vitesse.y * increment_temps / nb_ticks_sec

                dvx = self.acceleration.norm() * increment_temps / nb_ticks_sec * (self.direction * Coordonnees(1,0))
                dvy = self.acceleration.norm() * increment_temps / nb_ticks_sec * (self.direction * Coordonnees(0,1))

                acceleration_libre_x = 1 - (self.vitesse.x/self.voie)**4
                acceleration_libre_y = 1 - (self.vitesse.x/self.voie)**4
                acceleration_approche_x = 

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
