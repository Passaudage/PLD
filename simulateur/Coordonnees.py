import math 

class Coordonnees: 
    """
        Classe permettant de modéliser des coordonnées.
        # @author : Bonfante
    """

    def __init__(self, x=0, y=0): 
        self.x=x 
        self.y=y 

    def __eq__(self, vB): 
        """
            Test l'égalité de deux vecteurs.
        """
        return (self.x==vB.x) and (self.y==vB.y)    

    def __add__(self, vB):  
        """
                Retourne le vecteur somme.
        """
        return Coordonnees(self.x+vB.x,self.y+vB.y) 

    def __sub__(self, vB):  
        """
                Retourne le vecteur différence .
        """
        return Coordonnees(self.x-vB.x,self.y-vB.y) 

    def __mul__(self, c): 
        """
            Retourne le produit scalaire si le parametre est une coordonnée.
            Retourne le vecteur multiplé par un scalaire si c'est une valeur.
        """
        if isinstance(c,Coordonnees): 
            return  self.x*c.x+self.y*c.y
        else: 
            return Coordonnees(c*self.x,c*self.y)

    def __pow__(self, c): 
        """
            Retourne le produit vectoriel.
        """
        return self.x*c.y-self.y*c.x

    def __div__(self, c): 
        """
            Retourne le vecteur ayant subi une division scalaire.
        """
        return Coordonnees(self.x/c, self.y/c)

    def __abs__(self): 
        """
            Retourne la norme du vecteur.
        """
        return math.hypot(self.x, self.y)

    def normaliser(self):
        c = abs(self)
        if(c == 0): return Coordonnees(0,0)
        else: return Coordonnees(self.x/c, self.y/c)

    def __str__(self): 
        """
            Retourne la réprésentation de la coordonnée sous forme d'une chaîne.
        """
        return '('+str(self.x)+','+str(self.y)+')'

    def changer_repere(vec, origine, repere_x):
        vec_nv_x = math.cos(repere_x.x)*vec.x - math.sin(repere_x.y)*vec.y
        vec_nv_x -= origine.x

        vec_nv_y = math.sin(repere_x.x)*vec.x + math.cos(repere_x.y)*vec.y 
        vec_nv_y -= origine.y

        return Coordonnees(vec_nv_x, vec_nv_y)
