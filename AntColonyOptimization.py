import numpy as np
from MetaHeuristicFramework import VRP


class AntColonyOpt:
    def __init__(self, capacity, dist_matrix, goods, ants=10, max_iter=10000, evaporation_rate=0.5, alpha=1, beta=2):
        self.cities = list(range(1, len(goods)))
        self.alpha = alpha
        self.beta = beta
        self.evap_rate = evaporation_rate
        self.city_dist_matrix = dist_matrix
        self.pheromone_matrix = 2/(len(self.cities)*(len(self.cities)-1))*np.ones(self.city_dist_matrix.shape)
        self.goods = goods
        self.bestAnt = None
        self.truck_capacity = capacity
        self.visibility = np.divide(1, self.city_dist_matrix)
        self.visibility = np.where(self.visibility == np.inf, 0, self.visibility)
        self.ants = [Ant([], dist_matrix.shape[0]) for _ in range(ants)]
        self.aco_search(max_iter)

    def aco_search(self, max_iter):
        for i in range(max_iter):
            for ant in self.ants:
                path = self.find_path()
                ant.vrp = VRP(self.truck_capacity, self.city_dist_matrix, self.goods, path)
                if self.bestAnt is None or self.bestAnt.cost[0] > ant.vrp.cost[0]:
                    self.bestAnt = ant.vrp
                    print("Improvement Found!")
                    print("Iteration: ", i, "\nBest")
                    print(self.bestAnt)
            self.pheromone_matrix *= (1-self.evap_rate)
            for ant in self.ants:
                ant.update_pheromone(self.pheromone_matrix, self.evap_rate)

    def find_path(self):
        unvisited, vis, path, truck_load = self.cities.copy(), self.visibility.copy(), [], 0
        current_city = 0
        while unvisited:
            vis[:, current_city] = 0
            ro, tau = np.power(vis[current_city, :], self.beta), np.power(self.pheromone_matrix[current_city, :], self.alpha)
            denominator = np.sum(np.multiply(ro, tau))
            city_prob = [np.divide(ro[city] * tau[city], denominator) for city in unvisited]
            next_city = np.random.choice(unvisited, p=city_prob)
            truck_load += self.goods[next_city]
            if truck_load > self.truck_capacity:
                current_city, truck_load = 0, 0
                continue
            path.append(next_city)
            unvisited.remove(next_city)
            current_city = path[-1]
        return path


class Ant:
    def __init__(self, path, dim):
        self.path = path
        self.unvisited = list(range(1, dim))
        self.vrp = None

    def update_pheromone(self, phe_mat, evap_rate):
        cost = self.vrp.cost
        for t in self.vrp.trucks:
            city = t.route[0]
            for r in t.route:
                phe_mat[city][r] += evap_rate*(self.vrp.dist_matrix[city][r] / cost[0])
                phe_mat[r][city] += evap_rate*(self.vrp.dist_matrix[city][r] / cost[0])
                city = r
