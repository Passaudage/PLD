import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import cairo

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
		
		zone_dessin = Gtk.DrawingArea()
		zone_dessin.connect('draw', self.dessiner_tout)
		self.add(zone_dessin)
		self.show_all()

	def dessiner_tout(self, widget, cairo_context):
		print("Dessin !")

	def quit(self, a, b):
		# voir la doc, je ne sais pas à quoi correspondent ces deux arguments...
		Gtk.main_quit(a, b)

fenetre = Fenetre()
Gtk.main()
