from abc import ABCMeta

class controleAccess(metaclass=ABCMeta):
    @abstractmethod
    def estPassant():

class voiePrioritaire(controleAcces):
    def estPassant():
        return True
