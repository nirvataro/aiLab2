import numpy as np
import random
MaxSearches = 10000


class VRP:
    def __init__(self, capacity, dist_matrix, goods, config=None):
        self.trucks = [Truck(capacity)]
        self.max_capacity = capacity
        self.dist_matrix = dist_matrix
        self.goods = goods
        self.unvisited_cities = list(range(1, len(goods)))
        if config is None:
            self.config = self.generate_start_permutation_3NN()
        else:
            self.config = config
        self.cost = None
        self.update_path()
#         for city in self.config:
#             self.add_route(city)
#         self.add_route(0)
#         self.cost = self.calc_cost()


    def add_truck(self):
        self.trucks.append(Truck(self.max_capacity))

    def add_route(self, city):
        if self.trucks[-1].capacity - self.goods[city] < 0:
            self.trucks[-1].distance_travel += self.dist_matrix[self.trucks[-1].route[-1]][0]
            self.trucks[-1].route.append(0)
            self.add_truck()

        self.trucks[-1].capacity -= self.goods[city]
        self.trucks[-1].distance_travel += self.dist_matrix[self.trucks[-1].route[-1]][city]
        self.trucks[-1].route.append(city)
        if city != 0:
            self.unvisited_cities.remove(city)

    def calc_cost(self):
        total_cost = 0
        for t in self.trucks:
            total_cost += t.distance_travel
        return total_cost, len(self.trucks)


    def update_path(self):
        self.trucks = [Truck(self.max_capacity)]
        for city in self.config:
            self.add_route(city)
        self.add_route(0)
        self.cost = self.calc_cost()
        self.unvisited_cities = list(range(1, len(self.goods)))

    def __str__(self):
        string = "Route: \n"
        for i, t in enumerate(self.trucks):
            string += "Truck " + str(i + 1) + ": " + str(t.route) + "\n"
        return string + "Total Cost: " + str(self.cost) + "\n"

    def generate_start_permutation_3NN(self):
        permutation = []
        unvisited_cities = self.unvisited_cities.copy()
        cities = self.unvisited_cities.copy()
        current_city = 0
        while unvisited_cities:
            min1 = min2 = min3 = np.inf
            min1_city, min2_city, min3_city = 0, 0, 0
            for city in cities:
                dist = self.dist_matrix[current_city][city]
                if city != current_city and dist < min3 and city in unvisited_cities and city != 0:
                    min3 = dist
                    min3_city = city
                    if dist < min2:
                        min3, min2 = min2, min3
                        min3_city, min2_city = min2_city, min3_city
                        if min2 < min1:
                            min1, min2 = min2, min1
                            min1_city, min2_city = min2_city, min1_city
            choices = [min1_city, min2_city, min3_city]
            choices = list(filter(lambda x: x != 0, choices))
            city = random.choice(choices)
            permutation.append(city)
            unvisited_cities.remove(city)
        return np.array(permutation)


class Truck:
    def __init__(self, capacity):
        self.capacity = capacity
        self.distance_travel = 0
        self.route = [0]
