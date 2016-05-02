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
        if origine is None:
            vec_translate = vec
        else:
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

        if origine is None:
            origine = Coordonnees(0, 0)

        repere_y = Coordonnees(-repere_x.y, repere_x.x)
        vec_x_canon = origine.x + vec.x * repere_x.x + vec.y * repere_y.x
        vec_y_canon = origine.y + vec.x * repere_x.y + vec.y * repere_y.y

        return Coordonnees(vec_x_canon, vec_y_canon)

    def apply(vec_a, vec_b, fonction):
        return Coordonnees( fonction(vec_a.x, vec_b.x),
                            fonction(vec_a.y, vec_b.y))

    @staticmethod
    def se_coupent(d1, f1, d2, f2):
        axe_x = (f1 - d1).normaliser()
        d1_n = Coordonnees.changer_repere(d1, d1, axe_x)
        d2_n = Coordonnees.changer_repere(d2, d1, axe_x)
        f1_n = Coordonnees.changer_repere(f1, d1, axe_x)
        f2_n = Coordonnees.changer_repere(f2, d1, axe_x)

        liste_points = [d2_n, f2_n]
        tous_au_dessus = True
        tous_au_dessous = True
        tous_a_droite = True
        tous_a_gauche = True

        for point in liste_points:
            if point.x >= d1_n.x:
                tous_a_gauche = False
            if point.x <= f1_n.x:
                tous_a_droite = False
            if point.y <= 0:
                tous_au_dessus = False
            if point.y >= 0:
                tous_au_dessous = False 

        if tous_au_dessous or tous_au_dessous or tous_a_droite or tous_a_gauche:
            return False

        if f2_n.x == d2_n.x:
            return True

        a = (f2_n.y - d2_n.y)/(f2_n.x - d2_n.x)
        
        if a == 0:
            return True

        b = f2_n.y - a*f2_n.x

        x_inter = -b / a

        return (x_inter >= 0 and x_inter <= f1_n.x)
