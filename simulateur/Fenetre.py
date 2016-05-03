import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk


import Visualisateur
import main
import jacky
import DoubleCarrefour
import TripleCarrefour
import Apprentissage 

import Intersection
import Vehicule

import sys

def get_simulateur():

    sim = jacky.charger_simulateur()
    #sim = DoubleCarrefour.charger_simulateur()
    #~ sim = TripleCarrefour.charger_simulateur()

    return sim

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


    def quit(self, action, parametre):
        self.app.quitter_callback(action, parametre)


class Application(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)
        self.visual = None
        self.apprentissage = None

    def do_activate(self):
        self.win = Fenetre(self)
        self.win.show_all()

    def simuler_callback(self, action, parametre):
        if self.visual is None:
            sim = get_simulateur()
            self.def_visual(sim)

    def quitter_callback(self, action, parametre):
        if self.visual is not None:
            self.visual.notifier_fin()
        if self.apprentissage is not None:
            self.apprentissage.notifier_fin()
        sys.exit()

    def apprentissage_callback(self, action, parametre):
        if self.apprentissage is None:
            sim = get_simulateur()
            duree = 2400 # 10 minutes
            increment_simulateur_apprentissage = 10 # secondes
            self.apprentissage = Apprentissage.Apprentissage(sim,increment_simulateur_apprentissage,
             duree)
        else:
            if self.apprentissage.apprentissage_en_cours:
                self.apprentissage.terminated = True
            elif self.apprentissage.apprentissage_termine:
                # le but est d'afficher une simulation en prenant en compte
                # les changements de feux à partir du réseau de neurone
                print("On affiche la simulation basée sur l'apprentissage")
                
                #sim = get_simulateur()
                if self.apprentissage.simulateur is None:
                    sim = get_simulateur()

                sim = self.apprentissage.simulateur

                # on enregistre chaque réseau pour les intersections
                for intersection in self.apprentissage.reseaux_action:
                    intersection.reseau_neurone = self.apprentissage.reseaux_action[intersection]

                self.def_visual(sim)

    def charger_apprentissage_callback(self, action, parametre):

        sim = get_simulateur()

        reseaux = Apprentissage.restaurer_modele()

        intersections = {}

        for listener in sim.listeners:
            if type(listener) is Intersection.Intersection:
                intersections[str(listener.coordonnees)] = listener

        # on enregistre chaque réseau pour les intersections
        for intersection in reseaux:

            intersections[str(intersection.coordonnees)].reseau_neurone = reseaux[intersection]
            print("ok")

        self.def_visual(sim)

    def reset_callback(self, action, parametre):
        if self.visual is not None:

            if self.visual.thread_sim is not None:
                self.visual.notifier_fin()
                self.visual.thread_sim.join()


            Vehicule.Vehicule.liste_voitures = []
            self.visual.simulateur = get_simulateur();
            self.visual.intersections = []
            self.visual.troncons = []
            self.visual.recuperer_inter_troncons()
            self.visual.demarrer_simulation()


    def do_startup(self):
        Gtk.Application.do_startup(self)

        builder = Gtk.Builder()
        builder.add_from_file("menubar.ui")
        self.set_menubar(builder.get_object("menubar"))

        # action "simuler" de la barre de menu
        simuler_action = Gio.SimpleAction.new("simuler", None)
        simuler_action.connect("activate", self.simuler_callback)
        self.add_action(simuler_action)

        # action "apprentissage" de la barre de menu
        apprentissage_action = Gio.SimpleAction.new("apprentissage", None)
        apprentissage_action.connect("activate", self.apprentissage_callback)
        self.add_action(apprentissage_action)

        # action "charger_apprentissage" de la barre de menu
        charger_apprentissage_action = Gio.SimpleAction.new("charger_apprentissage", None)
        charger_apprentissage_action.connect("activate", self.charger_apprentissage_callback)
        self.add_action(charger_apprentissage_action)

        # action "charger_apprentissage" de la barre de menu
        reset_action = Gio.SimpleAction.new("reset", None)
        reset_action.connect("activate", self.reset_callback)
        self.add_action(reset_action)

        # action "quitter" de la barre de menu
        quitter_action = Gio.SimpleAction.new("quitter", None)
        quitter_action.connect("activate", self.quitter_callback)
        self.add_action(quitter_action)

    def def_visual(self, sim):

        self.sim = sim

        self.visual = Visualisateur.Visualisateur(self.sim, Fenetre.taille_x, Fenetre.taille_y)
        self.visual.demarrer_simulation()
        self.win.add(self.visual.zone_dessin)
        self.win.show_all()


app = Application()
app.run()
