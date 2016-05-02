#~ class Configuration: 
    #~ """
        #~ Classe permettant de modéliser la configuration d'un carrefour
        #~ # etats_feux : une chaine de caractère représentant les 12 bits des feux
        #~ # temps_validite : 0 court, 1 
        #~ # @author : Bonfante
    #~ """
#~ 
    #~ def __init__(self, etats_feux, temps_validite): 
        #~ self.etats_feux = etats_feux
        #~ self.temps_validite = temps_validite

configs = {}
configs[0] = ("000011110000",0)

print(configs)