import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import graphe.Interface

class Monitoring(Gtk.Window):

    taille_x = 800
    hauteur_graphe = 500
    hauteur_ecriture = 40
    def __init__(self, application, proto_data):
        Gtk.Window.__init__(self)
        self.set_title("Montoring")

        self.app = application
        self.data_init = proto_data

        #self.data_init = data_init
        self.hauteur_legende = len(proto_data) * Monitoring.hauteur_ecriture

        self.set_default_size(Monitoring.taille_x, self.hauteur_legende + Monitoring.hauteur_graphe)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.connect('delete-event', self.quit)

        self.def_visual()

        self.add(self.visual.zone_dessin)
        self.show_all()
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 7, "b": 1200})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5, "b": 1600})
        # self.visual.maj({"a": 5})
        # self.visual.maj({"a": 5, "b": 500})
        # self.visual.maj({"a": 5})
        # self.visual.maj({"a": 5})
        # self.visual.maj({"a": 5, "b": 1600, "random": 166})
        # self.visual.maj({"a": 5, "b": 1600, "random": 126})
        # self.visual.maj({"a": 5, "b": 1600, "random": 156})
        # self.visual.maj({"a": 5, "b": 1600, "random": 176})
        # self.visual.maj({"a": 5, "b": 1600, "random": 100})

    def def_visual(self):
        self.visual = graphe.Interface.Interface(self.data_init, Monitoring.taille_x, Monitoring.hauteur_graphe + self.hauteur_legende, Monitoring.hauteur_graphe)

    def quit(self, a, b):
        Gtk.main_quit(a, b)


#data = {"a":[2, 20, 60], "b":[100, 2000, 60] , "random": [100, 200, 3]}
#fenetre = Monitoring(data)
#Gtk.main()

