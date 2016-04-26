class SimulationManager:
    def __init__(self, grain):
        self.grain = grain
        self.temps = 0
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def avance_temps(self):
        self.temps += self.grain
        for listener in self.listeners:
            listener.notifie_temps(self.grain, self)

    def del_listener(self, listener):
        self.listeners.remove(listener)

#########################################################
# Classe de test
#########################################################
#class DummyListener:
#    def __init__(self, i):
#        self.i = i
#
#    def notifie_temps(self, temps, moteur):
#        print(self.i)
#
#x = SimulationManager(18)
#y = DummyListener(1)
#z = DummyListener(2)
#
#x.add_listener(y)
#x.add_listener(z)
#
#x.avance_temps()
#x.avance_temps()
#x.del_listener(y)
#x.avance_temps()
#x.avance_temps()
#x.del_listener(z)
#print('test')
#x.avance_temps()
#print('test2')
