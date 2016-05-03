class Graphe:

    def __init__(self, variables_min_max_nbpoints):
        self.variables_min_max_nbpoints = variables_min_max_nbpoints

        self.variables_points = {}

        for variable in self.variables_min_max_nbpoints.keys():
            self.variables_points[variable] = []



    def maj(self, nouveaux_points):
        for variable in self.variables_points.keys():
            if(variable in nouveaux_points.keys()):
                self.variables_points[variable].insert(0,nouveaux_points.get(variable))
            else:
                if(len(self.variables_points[variable]) >=1):
                    self.variables_points[variable].insert(0, self.variables_points[variable][0])
                else: self.variables_points[variable].append(0)

            nb_points = self.variables_min_max_nbpoints.get(variable)[2]
            if(len(self.variables_points[variable]) > nb_points):
                del self.variables_points.get(variable)[-1]

