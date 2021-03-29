import numpy as np
import random
from MetaHeuristicFramework import VRP


class SimulatedAnnealing:
    def __init__(self, capacity, dist_matrix, goods, start_temp=90, alpha=0.01):
        self.cities = list(range(1, len(goods)))
        self.city_dist_matrix = dist_matrix
        self.goods = goods
        self.truck_capacity = capacity
        self.saBest = VRP(capacity, dist_matrix, goods)
        self.sa_search(start_temp, alpha)

    def sa_search(self, temp, alpha):
        candidate, i = self.saBest, 0
        while temp > 0:
            n_hood = self.getNeighborhood(candidate)
            random_neighbor = random.choice(n_hood)
            chance = np.exp((candidate.cost[0] - random_neighbor.cost[0]) / temp)
            temp -= alpha
            if random_neighbor.cost[0] < self.saBest.cost[0]:
                self.saBest = random_neighbor
                print("Improvement Found!")
                print("Iteration: ", i, "\nBest")
                print(self.saBest)
            if random_neighbor.cost[0] < candidate.cost[0] or random.random() < chance:
                candidate = random_neighbor
            if not i % 1000:
                print(temp)
            i += 1

    def getNeighborhood(self, candidate):
        neighborhood = []
        for i in range(len(candidate.config)):
            for j in range(i + 1, len(candidate.config)):
                new_node = [i for i in candidate.config]
                new_node[i], new_node[j] = new_node[j], new_node[i]
                neighborhood.append(
                    VRP(self.truck_capacity, self.city_dist_matrix, self.goods, np.array(new_node)))
        return neighborhood

    def __str__(self):
        string = "Simulated Annealing:\nThe Best Route Found: \n"
        return string + str(self.saBest)
