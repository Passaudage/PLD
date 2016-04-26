import coordonnees

 class vehicule:
    acceleration = coordonnees(0,0)
    vitesse = coordonnees(0,0)
    est_arrete = False

    def __init__(self, max_acceleration, coordonnees, aggressivite, longueur, voie, prochaine_direction, racine):
        self.coordonnees = coordonnees
        self.max_acceleration = max_acceleration
        self.aggressivite = aggressivite
        self.longueur = longueur
        self.changeDirection(0,0)
        self.voie = voie
        self.prochaine_direction = prochaine_direction
        self.vehicule_precedent
        self.vehicule_suivant = []
        self.racine = racine
        self.direction
        self.voie_actuelle
        self.intersection_actuelle


    def changeDirection(self, x, y):
        self.direction = coordonnees(x, y)

    def avancerBoucle(pasTemporel):

        return False



    def calculerVitesse(self):

        return


    def notifie(self):
        return

    def avance_vehicule(self, vehicule_suivant):
        #fait avancer le vehicule
        return

    def set_vehicule_precedent(self, vehicule):
        self.vehicule_precedent = vehicule
        vehicule.set_vehicule_suivant(self)


    def set_vehicule_suivant(self, vehicule):
        self.vehicule_suivant.append(vehicule)

    def propager_racine(self):


        #suis je sur la bonne direction ?
	acceleration = coordonnees(0,0)
	vitesse = coordonnees(0,0)
	est_arrete = False
	self.vehicules_suivants = []
	self.simulateur


	def __init__(self, max_acceleration, coordonnees, longueur, voie, prochaine_direction, racine):
		self.coordonnees = coordonnees
		self.max_acceleration = max_acceleration
		self.longueur = longueur
		self.changeDirection(0,0)
		self.voie = voie
		self.prochaine_direction = prochaine_direction
		self.vehicule_precedent
		self.racine = racine
		self.direction
		self.voie_actuelle
		self.intersection_actuelle

		voiture_fin = self.voie.get_dernier_element()
		self.greffe_arbre(voiture_fin)


	def changeDirection(self, x, y):
		self.direction = coordonnees(x, y)

	def avancerBoucle(pasTemporel):

		return False



	def calculerVitesse(self):

		return


	def notifie_temps(self):
		#if (len(self.vehicules_suivants) == 0):
		return

	def avance_vehicule(self):
		self.vehicules_suivants.notifie_temps
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
