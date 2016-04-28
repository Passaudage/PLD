import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from SimulationManager import *
from Visualisateur import *

class Fenetre(Gtk.Window):
    """
        Classe de la fenêtre d'affichage
            # @author : Quentin
    """

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Visualisation")
        self.set_default_size(800,600)

        self.connect('delete-event', self.quit)
        
        self.def_visual()

        self.add(self.visual.zone_dessin)
        self.show_all()

    def def_visual(self):

        grain = 100

        self.sim = SimulationManager(grain)
        self.visual = Visualisateur(self.sim)

    def quit(self, a, b):
        # voir la doc, je ne sais pas à quoi correspondent ces deux arguments...
        Gtk.main_quit(a, b)

fenetre = Fenetre()
Gtk.main()
