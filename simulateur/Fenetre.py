import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import SimulationManager

import Visualisateur
import main

class Fenetre(Gtk.Window):
    """
        Classe de la fenêtre d'affichage
            # @author : Quentin
    """

    taille_x = 600
    taille_y = 600

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Visualisation")
        self.set_default_size(Fenetre.taille_x, Fenetre.taille_y)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.connect('delete-event', self.quit)
        
        self.def_visual()

        self.add(self.visual.zone_dessin)
        self.show_all()

    def def_visual(self):

        grain = 100

        self.sim = main.charger_simulateur()

        self.visual = Visualisateur.Visualisateur(self.sim, Fenetre.taille_x, Fenetre.taille_y)
        self.visual.demarrer_simulation()

    def quit(self, a, b):
        # voir la doc, je ne sais pas à quoi correspondent ces deux arguments...
        self.visual.notifier_fin()
        Gtk.main_quit(a, b)

fenetre = Fenetre()
Gtk.main()
