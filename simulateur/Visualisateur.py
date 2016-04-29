import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import Coordonnees
import Intersection

import Vehicule
import Troncon
import threading
import time

import random
import math

class Visualisateur: 
    """
        Classe de visualisation du traffic
            # zone_dessin : contexte pour dessiner via cairo
            # simulateur : permet de récupérer les infos sur les voitures
            # @author : Quentin
    """

    def __init__(self, simulateur, taille_x, taille_y):

        self.grain = 1 # en ticks
        self.simulateur = simulateur
        self.zone_dessin = Gtk.DrawingArea()
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.terminated = False

        self.zone_dessin.connect('draw', self.dessiner_tout)

        # récupérer la voirie (qui est fixe)
        self.intersections = []
        self.troncons = []

        for listener in self.simulateur.listeners:
            if type(listener) is Intersection.Intersection:
                self.intersections.append(listener)
                
                if listener.troncon_gauche is not None:
                    self.troncons.append(listener.troncon_gauche)
                if listener.troncon_droite is not None:
                    self.troncons.append(listener.troncon_droite)
                if listener.troncon_haut is not None:
                    self.troncons.append(listener.troncon_haut)
                if listener.troncon_bas is not None:
                    self.troncons.append(listener.troncon_bas)

        self.definir_limite()

        self.rotation = 0
        self.position = 300
        self.position_dec = True

    def notifier_fin(self):
        self.terminated = True

    def demarrer_simulation(self):
        self.thread_sim = threading.Thread(None, self.boucle_simulation)
        self.thread_sim.start()
        
        return

        self.thread_sim = threading.Thread(None, self.boucle_simulation)
        self.thread_sim.start()

        self.thread_dessin = threading.Thread(None, self.boucle_dessiner)
        self.thread_dessin.start()


    def boucle_simulation(self):
        
        while not self.terminated:
            for i in range(10):
                self.simulateur.avance_temps()
                self.rotation += 0.001 * 90 * 2 / 3.14159
                if self.position > 550 or self.position < 50:
                    self.position_dec = not self.position_dec
                self.position = self.position - 2 if self.position_dec else self.position + 2

            #self.dessiner_tout()
            time.sleep(self.grain / self.simulateur.nombre_ticks_seconde)

    def dessiner_tout(self, widget, cairo_context):
        #print("Dessin")

        self.cairo_context = cairo_context

        self.dessiner_voirie()
        self.dessiner_voitures()

        widget.queue_draw()

    def dessiner_voitures(self):
        """
            Cette  méthode dessine l'ensemble des voitures
        """
        
        self.cairo_context.set_source_rgba(0.1, 0, 0.8, 1)
        coord_test = self.echelle(Coordonnees.Coordonnees(6050, 7100))
        orientation = self.rotation
        longueur = self.fact_echelle * 350
        largeur = self.largeur_vehicule
        self.cairo_context.save()
        self.cairo_context.translate(coord_test.x, self.position)
        self.cairo_context.rotate(orientation) # en degrés
        self.cairo_context.translate(-largeur * 0.5, 0)
        self.cairo_context.rectangle(0, 0, largeur, longueur)
        self.cairo_context.fill()
        self.cairo_context.restore()

        self.cairo_context.set_source_rgba(1, 0, 0, 1)

        for voiture in Vehicule.Vehicule.liste_voitures:
            self.dessiner_voiture(voiture)

    def dessiner_voiture(self, voiture):

        coord = self.echelle(voiture.coordonnees)
        longueur = self.fact_echelle * voiture.longueur
        orientation = voiture.direction

        print("Dessin voiture :" + str(coord))
        
        angle = math.atan2(orientation.y, orientation.x)
        self.cairo_context.save()
        self.cairo_context.translate(coord.x, coord.y)
        self.cairo_context.rotate(angle + math.pi / 2) # en radiant
        self.cairo_context.translate(-self.largeur_vehicule * 0.5, 0)
        self.cairo_context.rectangle(0, 0, self.largeur_vehicule, longueur)
        self.cairo_context.fill()
        self.cairo_context.restore()


    def dessiner_voirie(self):
        
        for troncon in self.troncons:
            self.dessiner_troncon(troncon)

#        for intersection in self.intersections:
#            self.dessiner_intersection(intersection)


    def dessiner_troncon(self, troncon):

#        print(troncon.coordonnees_debut)
#        print(troncon.coordonnees_fin)

        vec_debut = self.echelle(troncon.coordonnees_debut)
        vec_fin = self.echelle(troncon.coordonnees_fin)
        largeur_voie = self.fact_echelle * Troncon.Troncon.const_largeur_voie
        largeur_voies = largeur_voie * (len(troncon.voies_sens1) + len(troncon.voies_sens2))

        self.cairo_context.save()
        self.cairo_context.set_source_rgba(0, 0, 0, 0.6)

        self.cairo_context.move_to(vec_debut.x, vec_debut.y)

        self.cairo_context.rel_line_to( vec_fin.x - vec_debut.x,
                                        vec_fin.y - vec_debut.y)

        self.cairo_context.set_line_width(largeur_voies)
        self.cairo_context.stroke()

        self.cairo_context.set_source_rgba(0, 0, 0, 1)
        self.cairo_context.move_to(vec_debut.x, vec_debut.y)
        self.cairo_context.rel_line_to( vec_fin.x - vec_debut.x,
                                        vec_fin.y - vec_debut.y)

        self.cairo_context.set_line_width(largeur_voie*0.15)
        self.cairo_context.stroke()

        dash = [self.fact_echelle * 200, self.fact_echelle * 150]
        distance = (vec_fin - vec_debut).__abs__()
        ndash = distance / (self.fact_echelle * 100)

        numero_voie = 1
        ajout_x = 0
        ajout_y = 0

        horizontal = False

        if troncon.voies_sens1[0].orientation.y == 0:
            # horizontal
            horizontal = True
            ajout_y = largeur_voie
        else:
            ajout_x = largeur_voie

        self.cairo_context.set_source_rgba(150, 150, 150, 1)

        for voie in troncon.voies_sens1[1:]:

            self.cairo_context.move_to( vec_debut.x + numero_voie * ajout_x,
                                        vec_debut.y + numero_voie * ajout_y)
            self.cairo_context.rel_line_to( vec_fin.x - vec_debut.x,
                                            vec_fin.y - vec_debut.y)
            self.cairo_context.set_dash(dash, ndash)
            self.cairo_context.set_line_width(largeur_voie*0.1)
            self.cairo_context.stroke()

            numero_voie += 1

        numero_voie = 1

        for voie in troncon.voies_sens2[1:]:

            self.cairo_context.move_to( vec_debut.x - numero_voie * ajout_x,
                                        vec_debut.y - numero_voie * ajout_y)
            self.cairo_context.rel_line_to( vec_fin.x - vec_debut.x,
                                            vec_fin.y - vec_debut.y)
            self.cairo_context.set_dash(dash, ndash)
            self.cairo_context.set_line_width(largeur_voie*0.1)
            self.cairo_context.stroke()

            numero_voie += 1

        # dessin des feux

        rayon_feu = 100

        if troncon.dir_voies_sens1["G"]:

            if horizontal:
                self.cairo_context.set_source_rgba(0.1, 1, 0.1, 1)
                self.cairo_context.arc( max(vec_debut.x, vec_fin.x), vec_debut.y,
                                        rayon_feu * self.fact_echelle, 0, 2*math.pi)
                self.cairo_context.fill()

        self.cairo_context.restore()

    def dessiner_intersection(self, intersection):
        # dessin des feux

        offset_feu = 10

        # pour chaque voie, on vérifie s'il existe un feu dans la direction 'G', 'D', 'H', 'B'
        # et on accumule la réponse

        directions = []

        for voie in intersection.entrantes:
            directions.extend([direction for direction in voie.directions if not direction in directions])

        self.cairo_context.restore()

        print("END")
        time.sleep(10)

    def echelle(self, vec):
        return (vec - self.min) * self.fact_echelle

    def definir_limite(self):
        """
            Calcule le min et le max en x et y pour mettre l'affichage à l'échelle.
        """

        self.min = None
        self.max = None

        if not self.troncons:
            raise Exception('Pas de troncons !')

        for troncon in self.troncons:
            if self.min is None:
                self.min = troncon.coordonnees_debut
            if self.max is None:
                self.max = troncon.coordonnees_debut

            self.min = Coordonnees.Coordonnees.apply(
                self.min, troncon.coordonnees_debut, min)
            self.max = Coordonnees.Coordonnees.apply(
                self.max, troncon.coordonnees_debut, max)
            self.min = Coordonnees.Coordonnees.apply(
                self.min, troncon.coordonnees_fin, min)
            self.max = Coordonnees.Coordonnees.apply(
                self.max, troncon.coordonnees_fin, max)

        #print(self.min)
        #print(self.max)

        diff_x = self.max.x - self.min.x
        diff_y = self.max.y - self.min.y

        self.fact_echelle = self.taille_x / diff_x if diff_x > diff_y else self.taille_y / diff_y

        self.largeur_vehicule = Vehicule.Vehicule.largeur * self.fact_echelle
        #print(self.fact_echelle)
