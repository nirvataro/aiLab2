import random
import numpy as np
from MetaHeuristicFramework import VRP
import time


class AntColonyOpt:
    def __init__(self, capacity, dist_matrix, goods, ants=100, search_time=120, evaporation_rate=0.5, alpha=1, beta=2, prob=0.1, output=False):
        self.goods = goods
        self.truck_capacity = capacity
        self.cities = list(range(1, len(goods)))
        self.city_dist_matrix = dist_matrix
        self.bestAnt = None
        self.pheromone_matrix = 0.1 * np.ones(self.city_dist_matrix.shape)
        self.visibility = np.zeros(self.city_dist_matrix.shape)
        np.divide(1., self.city_dist_matrix, out=self.visibility, where=self.city_dist_matrix!=0)
        self.ants = [Ant([], capacity, dist_matrix, goods) for _ in range(ants)]

        self.alpha = alpha
        self.beta = beta
        self.best_prob = prob
        self.evaporation_rate = evaporation_rate

        self.aco_search(search_time, output)

    def aco_search(self, search_time, output):
        no_improvement = 0
        end_time = time.time() + search_time
        time_left = end_time - time.time()
        while time_left > 0:
            for ant in self.ants:
                self.__find_path__(ant)
                ant.update_path()
                if self.bestAnt is None or self.bestAnt.cost[0] > ant.cost[0]:
                    self.bestAnt = ant.__copy__()
                    if output:
                        print("Improvement Found!")
                        print("Time: ", search_time - time_left, "\nBest")
                        print(self.bestAnt)
                    no_improvement = 0
            no_improvement += 1
            self.update_pheromone()
            if no_improvement > 100:
                self.pheromone_matrix = 0.1 * np.ones(self.city_dist_matrix.shape)
                no_improvement = 0
                if output:
                    print("Restart")
            time_left = end_time - time.time()

    def __find_path__(self, ant):
        unvisited, vis, path, truck_load = self.cities.copy(), self.visibility.copy(), [], 0
        current_city = 0 if not path else path[-1]
        while unvisited:
            city_prob = np.power(vis[current_city, unvisited], self.beta) * np.power(self.pheromone_matrix[current_city, unvisited], self.alpha)  # alpha = 1 remove power
            sum = np.sum(city_prob)
            city_prob = city_prob / sum

            if random.random() < self.best_prob:
                next_city = unvisited[np.argmax(city_prob)]
            else:
                next_city = np.random.choice(unvisited, p=city_prob)
            truck_load += self.goods[next_city]
            if truck_load > self.truck_capacity:
                current_city, truck_load = 0, 0
                continue
            path.append(next_city)
            unvisited.remove(next_city)
            current_city = path[-1]
            # local update pheromone
            self.pheromone_matrix[current_city, next_city] = (1-self.evaporation_rate) + self.evaporation_rate*(ant.dist_matrix[current_city][next_city] / ant.cost[0])
        ant.path = path
        ant.config = path

    def update_pheromone(self):
        self.pheromone_matrix *= (1 - self.evaporation_rate)
        cost = self.bestAnt.cost
        for t in self.bestAnt.trucks:
            city = t.route[0]
            for r in t.route:
                self.pheromone_matrix[city][r] += self.evaporation_rate*(self.city_dist_matrix[city][r] / cost[0])
                self.pheromone_matrix[r][city] += self.evaporation_rate*(self.city_dist_matrix[city][r] / cost[0])
                city = r

    def __str__(self):
        return "Ant Colony Optimization:\nThe Best Route Found:\n" + str(self.bestAnt)


class Ant(VRP):
    def __init__(self, path, capacity, dist_matrix, goods, config=None):
        super().__init__(capacity, dist_matrix, goods, config=config)
        self.path = path
        self.unvisited = list(range(1, len(goods)))

    def __copy__(self):
        return Ant(self.path, self.max_capacity, self.dist_matrix, self.goods, config=self.path)

    def __str__(self):
        string = "Route: \n"
        for i, t in enumerate(self.trucks):
            string += "Truck " + str(i + 1) + ": " + str(t.route) + "\n"
        return string + "Total Cost: " + str(self.cost) + "\n"

