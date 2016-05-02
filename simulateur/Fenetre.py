import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

import SimulationManager

import Visualisateur
import main
import jacky
import DoubleCarrefour
import TripleCarrefour

menu_xml="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="menubar">
    <section>
      <attribute name="label" translatable="yes">Change label</attribute>
      <item>
        <attribute name="label">Test001</attribute>
      </item>
    </section>
</interface>
"""

# <attribute name="action">win.change_label</attribute>


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


    def quit(self, a, b):
        # voir la doc, je ne sais pas à quoi correspondent ces deux arguments...
        self.app.visual.notifier_fin()


class Application(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        self.win = Fenetre(self)
        self.win.show_all()

    def simuler_callback(self, action, parameter):
        self.def_visual()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        builder = Gtk.Builder()
        builder.add_from_file("menubar.ui")
        self.set_menubar(builder.get_object("menubar"))

        # action "simuler" de la barre de menu
        simuler_action = Gio.SimpleAction.new("simuler", None)
        simuler_action.connect("activate", self.simuler_callback)
        self.add_action(simuler_action)

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
