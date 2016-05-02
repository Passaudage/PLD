import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

import SimulationManager

import Visualisateur
import main
import jacky
import DoubleCarrefour
import TripleCarrefour

import sys

class Fenetre(Gtk.ApplicationWindow):
    """
        Classe de la fenêtre d'affichage
            # @author : Quentin
    """

    taille_x = 600
    taille_y = 600

    def __init__(self, app):
        Gtk.Window.__init__(self, application = app)

        self.app = app
        self.set_title("Visualisation")
        self.set_default_size(Fenetre.taille_x, Fenetre.taille_y)
        self.set_position(Gtk.WindowPosition.CENTER)     

        self.connect('delete-event', self.quit)


    def quit(self, action, parameter):
        self.app.quitter_callback(action, parameter)


class Application(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)
        self.visual = None

    def do_activate(self):
        self.win = Fenetre(self)
        self.win.show_all()

    def simuler_callback(self, action, parameter):
        self.def_visual()

    def quitter_callback(self, action, parameter):
        if self.visual is not None:
            self.visual.notifier_fin()
        sys.exit()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        builder = Gtk.Builder()
        builder.add_from_file("menubar.ui")
        self.set_menubar(builder.get_object("menubar"))

        # action "simuler" de la barre de menu
        simuler_action = Gio.SimpleAction.new("simuler", None)
        simuler_action.connect("activate", self.simuler_callback)
        self.add_action(simuler_action)

        # action "quitter" de la barre de menu
        quitter_action = Gio.SimpleAction.new("quitter", None)
        quitter_action.connect("activate", self.quitter_callback)
        self.add_action(quitter_action)

    def def_visual(self):
        #~ self.sim = jacky.charger_simulateur()
        #~ self.sim = DoubleCarrefour.charger_simulateur()
        self.sim = TripleCarrefour.charger_simulateur()

        self.visual = Visualisateur.Visualisateur(self.sim, Fenetre.taille_x, Fenetre.taille_y)
        self.visual.demarrer_simulation()
        self.win.add(self.visual.zone_dessin)
        self.win.show_all()


app = Application()
app.run()
