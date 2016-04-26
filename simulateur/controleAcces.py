from abc import ABCMeta

class controle_access(metaclass=ABCMeta):
    @abstractmethod
    def est_passant():
    @abstractmethod
    def notifie_temps(self, temps, simulation_manager):

class voie_prioritaire(controle_access):
    def est_passant():
        return True
    def notifie_temps(self, temps, simulation_manager):
        pass
