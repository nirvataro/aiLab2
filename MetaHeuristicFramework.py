
MaxSearches = 10000


class VRP:
    def __init__(self, capacity, dist_matrix, goods, config):
        self.trucks = [Truck(capacity)]
        self.max_capacity = capacity
        self.dist_matrix = dist_matrix
        self.goods = goods
        self.unvisited_cities = list(range(1, len(goods)))
        self.config = config
        for city in self.config:
            self.add_route(city)
        self.add_route(0)
        self.cost = self.calc_cost()

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

    def __str__(self):
        string = "My Route: \n"
        for i, t in enumerate(self.trucks):
            string += "Truck " + str(i + 1) + ": " + str(t.route) + "\n"
        return string + "Total Cost: " + str(self.cost) + "\n"

class Truck:
    def __init__(self, capacity):
        self.capacity = capacity
        self.distance_travel = 0
        self.route = [0]
