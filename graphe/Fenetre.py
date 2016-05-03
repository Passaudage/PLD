import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import Interface

class Fenetre(Gtk.Window):

    taille_x = 800
    hauteur_graphe = 500
    hauteur_ecriture = 40
    def __init__(self, data_init):
        Gtk.Window.__init__(self)
        self.set_title("Tableau de bord")

        self.data_init = data_init
        self.hauteur_legende = len(data_init.keys())*Fenetre.hauteur_ecriture

        self.set_default_size(Fenetre.taille_x, self.hauteur_legende + Fenetre.hauteur_graphe)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.connect('delete-event', self.quit)

        self.def_visual()

        self.add(self.visual.zone_dessin)
        self.show_all()
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 7, "b": 1200})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})
        self.visual.maj({"a": 5, "b": 1600})

    def def_visual(self):

        self.visual = Interface.Interface(self.data_init, Fenetre.taille_x, Fenetre.hauteur_graphe + self.hauteur_legende, Fenetre.hauteur_graphe)

    def quit(self, a, b):
        # voir la doc, je ne sais pas à quoi correspondent ces deux arguments...
        Gtk.main_quit(a, b)

data = {"a":[2, 20, 60], "b":[100, 2000, 60] }
fenetre = Fenetre(data)
Gtk.main()

