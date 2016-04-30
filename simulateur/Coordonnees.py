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

    def __truediv__(self, c): 
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
        """
            vec : le vecteur a changer
            origine : origine du repère cible
            repere_x : vecteur unitaire x du repère cible
        """
        vec_translate = vec - origine
        repere_y = Coordonnees(-repere_x.y, repere_x.x)
        
        vec_nv_x = vec_translate * repere_x
        vec_nv_y = vec_translate * repere_y
        
        return Coordonnees(vec_nv_x, vec_nv_y)

    def inv_changer_repere(vec, origine, repere_x):
        """
            Pour retourner dans le repere canonique depuis un repere 
            defini par une translation origine et un axe x repere_x
        """
        repere_y = Coordonnees(-repere_x.y, repere_x.x)
        vec_x_canon = origine.x + vec.x * repere_x.x + vec.y * repere_y.x
        vec_y_canon = origine.y + vec.x * repere_x.y + vec.y * repere_y.y

        return Coordonnees(vec_x_canon, vec_y_canon)

    def apply(vec_a, vec_b, fonction):
        return Coordonnees( fonction(vec_a.x, vec_b.x),
                            fonction(vec_a.y, vec_b.y))

