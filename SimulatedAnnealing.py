import numpy as np
import random
from MetaHeuristicFramework import VRP
import time

class SimulatedAnnealing:
    def __init__(self, capacity, dist_matrix, goods, search_time=120):
        self.cities = list(range(1, len(goods)))
        self.city_dist_matrix = dist_matrix
        self.goods = goods
        self.truck_capacity = capacity
        self.saBest = VRP(capacity, dist_matrix, goods)
        self.sa_search(search_time)

    def sa_search(self, search_time):
        candidate = self.saBest
        end_time = time.time() + search_time
        time_left = end_time - time.time()
        i = 0
        while time_left > 0:
            time_left = end_time - time.time()
            temp = 90 * time_left / search_time
            random_neighbor = self.getRandomNeighborhood(candidate)
            if temp < 0.01:
                chance = 0
            else:
                chance = np.exp((candidate.cost[0] - random_neighbor.cost[0]) / temp)
            if random_neighbor.cost[0] < self.saBest.cost[0]:
                self.saBest = random_neighbor
                print("Improvement Found!")
                print("Iteration: ", i, "\nTime: ", search_time-time_left, "\nBest:")
                print(self.saBest)
            if random_neighbor.cost[0] < candidate.cost[0] or random.random() < chance:
                candidate = random_neighbor
            i += 1
        print("Timed Out")

    def getRandomNeighborhood(self, candidate):
        index_ij = random.sample(self.cities, 2)
        index_ij.sort()
        i_ind, j_ind = index_ij[0] - 1, index_ij[1] - 1
        neigh_config = candidate.config.copy()
        neigh_config[j_ind], neigh_config[i_ind] = candidate.config[i_ind], candidate.config[j_ind]
        return VRP(self.truck_capacity, self.city_dist_matrix, self.goods, neigh_config)

    def __str__(self):
        string = "Simulated Annealing:\nThe Best Route Found: \n"
        return string + str(self.saBest)
