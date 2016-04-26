from abc import ABCMeta

class controleAccess(metaclass=ABCMeta):
    @abstractmethod
    def estPassant():
    @abstractmethod
    def notifie_temps(self, temps, simulation_manager):

class voiePrioritaire(controleAcces):
    def estPassant():
        return True
    def notifie_temps(self, temps, simulation_manager):
        pass
