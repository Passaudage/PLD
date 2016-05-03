class Graphe:

    def __init__(self, variables_min_max_nbpoints):
        self.variables_min_max_nbpoints = variables_min_max_nbpoints

        self.variables_points = {}

        for variable in self.variables_min_max_nbpoints.keys():
            self.variables_points[variable] = []



    def maj(self, nouveaux_points):
        for variable in nouveaux_points.keys():
            self.variables_points[variable].append(nouveaux_points.get(variable))
            nb_points = self.variables_min_max_nbpoints.get(variable)[2]
            if(len(self.variables_points[variable]) > nb_points):
                del self.variables_points.get(variable)[-1]

