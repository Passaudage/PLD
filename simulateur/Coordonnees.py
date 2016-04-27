import math

class Coordonnees:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
	 
	def add(self,co2):
		self.x += co2.x
		self.y += co2.y
		
	def sub(self,co2):
		self.x -= co2.x
		self.y -= co2.y
		
	def addition(co,co2):
		toRet = Coordonnees(co.x+co2.x,co.y+co2.y)
		return toRet
		
	def soustraction(co,co2):
		toRet = Coordonnees(co.x-co2.x,co.y-co2.y)
		return toRet
		
	def __mul__(self,co):
		return Coordonnees(self.x-co.x,self.y-co.y)
		
	def norme(self):
		return math.sqrt(self.produit_scalaire(self))

	def produit_scalaire(self,co2):
		return self.x*co2.x+self.y*co2.y

	def mult(self,k):
		return Coordonnees(self.x*k, self.y*k)
		
	def normaliser(self):
		return Coordonnes(self.x/self.norme(), self.y/self.norme())
