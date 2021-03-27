import random


MaxSearches = 10000


class VRP:
    def __init__(self, capacity, dist_matrix, goods):
        self.trucks = [Truck(capacity)]
        self.max_capacity = capacity
        self.dist_matrix = dist_matrix
        self.goods = goods
        self.unvisited_cities = list(range(len(goods)))

    def add_truck(self):
        self.trucks.append(Truck(self.max_capacity))

    def add_route(self, city):
        if self.trucks[-1].capacity - self.goods[city] < 0:
            self.trucks[-1].route.append(0)
            self.trucks[-1].distance_travel += self.dist_matrix[self.trucks[-1].route[-1]][0]
            self.add_truck()

        self.trucks[-1].capacity -= self.goods[city]
        self.trucks[-1].distance_travel += self.dist_matrix[self.trucks[-1].route[-1]][city]
        self.trucks[-1].route.append(city)
        self.unvisited_cities.remove(city)

    def cost(self):
        total_cost = 0
        for t in self.trucks:
            total_cost += t.distance_travel
        return total_cost, len(self.trucks)


class Truck:
    def __init__(self, capacity):
        self.capacity = capacity
        self.distance_travel = 0
        self.route = [0]


def generateInitialSolution(capacity, dist_matrix, goods):
    vrp_generate = VRP(capacity, dist_matrix, goods)
    while vrp_generate.unvisited_cities:
        vrp_generate.add_route(random.choice(vrp_generate.unvisited_cities))

    return vrp_generate


def IteratedLocalSearch(capacity, dist_matrix, goods):
    s = generateInitialSolution(capacity, dist_matrix, goods)
    s_star = s
    for k in MaxSearches:
        s = LocalSearch(f, N, L, S, s)
        if s.cost < s_star.cost:
            s_star = s
        s = GenerateNewSolution(s)
    return s_star