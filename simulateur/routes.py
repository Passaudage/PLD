import coordonnees
import controleAcces

class intersection:
    

class voie:
    def __init__(self):
        self.intersectionsAccessibles = []

    def setTroncon(self, troncon):
        self.troncon = troncon


class troncon:
    def __init__(self, tete, queue):
        self.tete = tete
        self.queue = queue
