import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import graphe.Graphe
import math

import time

class Interface:

    couleurs = {7:(1,0,0.4), 6: (1,87/255,2/255), 5:(0, 168/255, 253/255),
                4: (0, 33/255, 71/255), 3: (80/255, 125/255, 42/255),
                2:(1, 215/255, 0), 1:(197/255, 118/255, 111/255)}


    marge = 10
    def __init__(self, variables_min_max_nbpoint, taille_x, taille_y, hauteur_graphe):

        self.variables_min_max_nb_points = variables_min_max_nbpoint
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.hauteur_graphe = hauteur_graphe
        self.hauteur_legende = taille_y - hauteur_graphe

        self.zone_dessin = Gtk.DrawingArea()
        self.origine_graphe = (Interface.marge, self.hauteur_legende+Interface.marge)
        self.longueur_axe_abscisses = taille_x-2*Interface.marge
        self.longueur_axe_ordonnees = taille_y - self.hauteur_legende - 2*Interface.marge

        self.set_couleurs(self.variables_min_max_nb_points.keys())

        self.graphe = graphe.Graphe.Graphe(self.variables_min_max_nb_points)
        self.zone_dessin.connect('draw', self.dessiner)


    def dessiner(self, widget, cairo_context):

        self.cairo_context = cairo_context

        self.cairo_context.save()
        self.cairo_context.translate(0, self.taille_y)
        self.cairo_context.scale(1, -1)
        self.dessiner_axes()
        self.dessiner_graphe()
        self.dessiner_legende()
        self.cairo_context.restore()

        widget.queue_draw()


    def dessiner_graphe(self):
        try:
            for variable in self.graphe.variables_points.keys():

                couleur = self.variables_couleurs.get(variable)
                self.cairo_context.set_source_rgba(couleur[0], couleur[1], couleur[2], 1)

                nb_points = self.variables_min_max_nb_points.get(variable)[2]-1

                iter_value = iter(self.graphe.variables_points.get(variable))
                x_premier_point = Interface.marge + self.longueur_axe_abscisses
                y_premier_point = self.mettre_a_echelle(next(iter_value), variable)
                point_precedent = (x_premier_point, y_premier_point+self.origine_graphe[1])
                self.cairo_context.arc(x_premier_point, y_premier_point + self.origine_graphe[1], 2, 0, 2 * math.pi)
                self.cairo_context.fill()

                point_dessine = 1
                for value in iter_value:
                    x = Interface.marge + (self.longueur_axe_abscisses - (point_dessine/nb_points*self.longueur_axe_abscisses))
                    y = self.mettre_a_echelle(value, variable)
                    self.cairo_context.arc(x, y + self.origine_graphe[1], 2, 0, 2 * math.pi)
                    self.cairo_context.fill()

                    self.cairo_context.move_to(point_precedent[0], point_precedent[1])
                    self.cairo_context.line_to(x, y+self.origine_graphe[1])
                    point_precedent = (x, y+ self.origine_graphe[1])
                    self.cairo_context.stroke()
                    point_dessine+=1
        except StopIteration:
            pass

    def dessiner_legende(self):

        self.cairo_context.scale(1, -1)
        self.cairo_context.translate(0, -self.taille_y)
        self.cairo_context.move_to(Interface.marge, self.hauteur_graphe)
        index1 = 1
        index2 = 0
        for variable in self.variables_min_max_nb_points.keys():
            self.cairo_context.move_to(Interface.marge, self.hauteur_graphe + index1 * 25 + index2 * 15)
            couleur = self.variables_couleurs.get(variable)
            self.cairo_context.set_source_rgba(couleur[0], couleur[1], couleur[2], 1)
            #self.cairo_context.select_font_face("Georgia", self.cairo_context.CAIRO_FONT_SLANT_NORMAL, self.cairo_context.CAIRO_FONT_WEIGHT_BOLD)
            self.cairo_context.set_font_size(15)
            text = variable + " " + " min : " + str(self.variables_min_max_nb_points.get(variable)[0]) \
                   + " max : " + str(self.variables_min_max_nb_points.get(variable)[1])
            self.cairo_context.show_text(text)
            index1+=1
            index2+=1

    def dessiner_axes(self):
        self.cairo_context.set_source_rgba(0, 0, 0, 1)

        #axe des abscisses
        self.cairo_context.move_to(self.origine_graphe[0], self.origine_graphe[1] )
        self.cairo_context.line_to(self.origine_graphe[0]+self.longueur_axe_abscisses, self.origine_graphe[1] )

        #axe des ordonnées
        self.cairo_context.move_to(self.origine_graphe[0], self.origine_graphe[1] )
        self.cairo_context.line_to(self.origine_graphe[0], self.origine_graphe[1] + self.longueur_axe_ordonnees)

        self.cairo_context.stroke()

    def maj(self, nouveaux_points):
        self.graphe.maj(nouveaux_points)

    def set_couleurs(self, variables):
        self.variables_couleurs = {}
        i = 1
        for variable in variables:
            self.variables_couleurs[variable] = Interface.couleurs[i]
            i+=1

    def mettre_a_echelle(self, y, variable):
        return (y-self.variables_min_max_nb_points.get(variable)[0])/(self.variables_min_max_nb_points.get(variable)[1]-self.variables_min_max_nb_points.get(variable)[0])*self.longueur_axe_ordonnees


