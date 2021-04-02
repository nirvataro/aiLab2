import random
import numpy as np
from MetaHeuristicFramework import VRP


class AntColonyOpt:
    def __init__(self, capacity, dist_matrix, goods, ants=10, max_iter=10000, evaporation_rate=0.5, alpha=1, beta=2, prob=0.1):
        self.goods = goods
        self.truck_capacity = capacity
        self.cities = list(range(1, len(goods)))
        self.city_dist_matrix = dist_matrix

        self.bestAnt = None
        self.pheromone_matrix = 2/(len(self.cities)*(len(self.cities)-1))*np.ones(self.city_dist_matrix.shape)
        self.visibility = np.divide(1, self.city_dist_matrix)
        self.visibility = np.where(self.visibility == np.inf, 0, self.visibility)
        self.ants = [Ant([], capacity, dist_matrix, goods) for _ in range(ants)]

        self.alpha = alpha
        self.beta = beta
        self.best_prob = prob
        self.evaporation_rate = evaporation_rate

        self.aco_search(max_iter)

    def aco_search(self, max_iter):
        for i in range(max_iter):
            for ant in self.ants:
                self.__find_path__(ant)
                ant.update_path()
                if self.bestAnt is None or self.bestAnt.cost[0] > ant.cost[0]:
                    self.bestAnt = ant
                    print("Improvement Found!")
                    print("Iteration: ", i, "\nBest")
                    print(str(self.bestAnt))
            self.update_pheromone()

    def __find_path__(self, ant):
        unvisited, vis, path, truck_load = ant.unvisited, self.visibility.copy(), ant.path, 0
        current_city = 0 if not path else path[-1]
        while unvisited:
            city_prob = np.power(vis[current_city, unvisited], self.beta) * np.power(self.pheromone_matrix[current_city, unvisited], self.alpha)  # alpha = 1 remove power
            city_prob = city_prob / np.sum(city_prob)

            if random.random() < self.best_prob:
                next_city = unvisited[np.argmax(city_prob)]
            else:
                N = len(unvisited)
                city_prob = city_prob/np.sum(city_prob)
                while True:
                    ind = int(N * random.random())
                    if random.random() <= city_prob[ind]:
                        next_city = unvisited[ind]
                        break
            truck_load += self.goods[next_city]
            if truck_load > self.truck_capacity:
                current_city, truck_load = 0, 0
                continue
            path.append(next_city)
            unvisited.remove(next_city)
            current_city = path[-1]
            # local update pheromone
            self.pheromone_matrix[current_city, next_city] = (1-self.evaporation_rate) + self.evaporation_rate*(ant.dist_matrix[current_city][next_city] / ant.cost[0])

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


class Ant(VRP):
    def __init__(self, path, capacity, dist_matrix, goods):
        super().__init__(capacity, dist_matrix, goods)
        self.path = path
        self.unvisited = list(range(1, len(goods)))

    def __str__(self):
        string = "Route: \n"
        for i, t in enumerate(self.trucks):
            string += "Truck " + str(i + 1) + ": " + str(t.route) + "\n"
        return string + "Total Cost: " + str(self.cost) + "\n"



# vis[:, current_city] = 0
            # ro, tau = np.power(vis[current_city, :], self.beta), np.power(self.pheromone_matrix[current_city, :], self.alpha)
            # denominator = np.sum(np.multiply(ro, tau))
            # city_prob = [np.divide(ro[city] * tau[city], denominator) for city in unvisited]
            # next_city = np.random.choice(unvisited, p=city_prob)