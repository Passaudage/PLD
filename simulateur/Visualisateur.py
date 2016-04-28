import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Coordonnees import *
import Intersection

import Vehicule

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


    def dessiner_tout(self, widget, cairo_context):
        self.cairo_context = cairo_context

        self.dessiner_voirie()
        #self.dessiner_voitures()

        widget.queue_draw()

    def dessiner_voitures(self):
        """
            Cette  méthode dessine l'ensemble des voitures
        """
        # couleur d'une voiture
        self.cairo_context.set_source_rgba(0, 0, 70, 0.5)

        coord_test = Coordonnees(100, 100)
        orientation = 0
        longueur = 50

        self.dessiner_voiture(coord_test, orientation, longueur);
        self.dessiner_voiture(coord_test, orientation, longueur);

    def dessiner_voiture(self, coord, orientation, longueur):

        self.cairo_context.save()

        print("dessin !")
        #self.cairo_context.arc(0, 0, 50, 0, 0)
        self.cairo_context.translate(coord.x, coord.y)
        self.cairo_context.rotate(orientation) # en degrés

        self.cairo_context.rectangle(0, 0, Vehicule.largeur, longueur)
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

        print("intersection")

        self.cairo_context.save()

        self.cairo_context.move_to( troncon.coordonnees_debut.x,
                                    troncon.coordonnees_debut.y)

        self.cairo_context.rel_line_to( troncon.coordonnees_fin.x,
                                        troncon.coordonnees_fin.y)


        self.cairo_context.restore()

        return

    def definir_limite(self):
        """
            Calcule le min et le max en x et y pour mettre l'affichage à l'échelle.
        """

        self.min = None
        self.max = None

        for troncon in self.troncons:
            if self.min is None:
                troncon.coordonnees_debut
            if self.max is None:
                troncon.coordonnees_fin

            self.min = Coordonnees.apply(self.min, troncon.coordonnees_debut, min)
            self.max = Coordonnees.apply(self.max, troncon.coordonnees_debut, max)
            self.min = Coordonnees.apply(self.min, troncon.coordonnees_fin, min)
            self.max = Coordonnees.apply(self.max, troncon.coordonnees_fin, max)

        print(self.min)
        exit(0)
