import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Coordonnees import *

import Vehicule

class Visualisateur: 
    """
        Classe de visualisation du traffic
            # zone_dessin : contexte pour dessiner via cairo
            # simulateur : permet de récupérer les infos sur les voitures
            # @author : Quentin
    """

    def __init__(self, simulateur):

        self.grain = 1 # en ticks
        self.simulateur = simulateur
        self.zone_dessin = Gtk.DrawingArea()

        self.zone_dessin.connect('draw', self.dessiner_tout)

    def dessiner_tout(self, widget, cairo_context):
        self.cairo_context = cairo_context

        self.dessiner_voitures()

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

        self.cairo_context.rectangle(0, 0, Vehicule.Vehiculelargeur, longueur)
        self.cairo_context.fill()

        self.cairo_context.restore()

        return

    def dessiner_voirie(self):
        # on récupère les intersections, tronçons, etc.
        return

    def dessiner_intersection(self):

        return
