import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import Coordonnees
import Intersection

import Vehicule
import Troncon
import threading

class Visualisateur: 
    """
        Classe de visualisation du traffic
            # zone_dessin : contexte pour dessiner via cairo
            # simulateur : permet de récupérer les infos sur les voitures
            # @author : Quentin
    """

    def __init__(self, simulateur, taille_x, taille_y):

        self.grain = 10 # en ticks
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
            if type(listener) is Intersection:
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

    def notifier_fin(self):
        self.terminated = True

    def demarrer_simulation(self):
        self.thread_sim = threading.Thread(None, boucle_simulation)
        self.thread_sim.start()
        
        return

        self.thread_sim = threading.Thread(None, boucle_simulation)
        self.thread_sim.start()

        self.thread_dessin = threading.Thread(None, boucle_dessiner)
        self.thread_dessin.start()


    def boucle_simulation(self):
        
        while not self.terminated:
            for i in range(1):
                self.simulateur.avance_temps()

            self.dessiner_tout()
            threading.sleep(self.grain / self.simulateur.nombre_ticks_seconde)


    def boucle_dessiner(self):

        while True:
            self.dessiner_tout()

    def dessiner_tout(self, widget, cairo_context):
        self.cairo_context = cairo_context

        self.dessiner_voirie()
        self.dessiner_voitures()

        widget.queue_draw()

    def dessiner_voitures(self):
        """
            Cette  méthode dessine l'ensemble des voitures
        """
        # couleur d'une voiture
        self.cairo_context.set_source_rgba(0, 0, 70, 0.5)

        coord_test = Coordonnees(6050, 7100)
        orientation = 0
        longueur = 350

        self.dessiner_voiture(coord_test, orientation, longueur);

        return

        for voiture in liste_voitures:
            dessiner_voiture()

    def dessiner_voiture(self, voiture):
        #coord, orientation, longueur):

        coord = self.echelle(voiture.coordonnees)
        longueur = self.fact_echelle * voiture.longueur

        self.cairo_context.save()

        print("dessin !")
        
        self.cairo_context.translate(coord.x, coord.y)
        self.cairo_context.rotate(orientation) # en degrés

        self.cairo_context.rectangle(0, 0, Vehicule.largeur, longueur)

        #self.cairo_context.arc(0, 0, 50, 0, 0)
        self.cairo_context.fill()

        self.cairo_context.restore()

    def dessiner_voirie(self):
        
        for intersection in self.intersections:
            self.dessiner_intersection(intersection)

        for troncon in self.troncons:
            self.dessiner_troncon(troncon)
        

    def dessiner_intersection(self, intersection):
        return

    def dessiner_troncon(self, troncon):

        self.cairo_context.save()

        print(troncon.coordonnees_debut)
        print(troncon.coordonnees_fin)

        vec_debut = self.echelle(troncon.coordonnees_debut)
        vec_fin = self.echelle(troncon.coordonnees_fin)
        largeur_voie = self.fact_echelle * Troncon.Troncon.const_largeur_voie
        largeur_voie *= len(troncon.voies_sens1) + len(troncon.voies_sens2)

        self.cairo_context.set_source_rgba(0, 0, 0, 0.6)

        self.cairo_context.move_to( vec_debut.x,
                                    vec_debut.y)

        self.cairo_context.rel_line_to( vec_fin.x - vec_debut.x,
                                        vec_fin.y - vec_debut.y)

        self.cairo_context.set_line_width(largeur_voie)
        self.cairo_context.stroke()

        self.cairo_context.restore()

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

            self.min = Coordonnees.apply(self.min, troncon.coordonnees_debut, min)
            self.max = Coordonnees.apply(self.max, troncon.coordonnees_debut, max)
            self.min = Coordonnees.apply(self.min, troncon.coordonnees_fin, min)
            self.max = Coordonnees.apply(self.max, troncon.coordonnees_fin, max)

        print(self.min)
        print(self.max)

        diff_x = self.max.x - self.min.x
        diff_y = self.max.y - self.min.y

        self.fact_echelle = self.taille_x / diff_x if diff_x > diff_y else self.taille_y / diff_y


        print(self.fact_echelle)
