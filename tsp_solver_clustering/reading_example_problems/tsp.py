class Tsp:
    def __init__(self, name, cities, best_route):
        self.name = name
        self.cities = cities
        self.best_route = best_route


class TspSubproblem:
    def __init__(self, name, cities, center):
        self.name = name
        self.cities = cities
        self.center = center

    def __repr__(self):
        return str(self.name)
