import numpy as np
import random
from MetaHeuristicFramework import VRP

class SimulatedAnnealing:
    def __init__(self, capacity, dist_matrix, goods, start_temp=10000, maxIter=10000, alpha=0.95):
        self.cities = list(range(1, len(goods)))
        self.city_dist_matrix = dist_matrix
        self.goods = goods
        self.truck_capacity = capacity
        self.saBest = VRP(capacity, dist_matrix, goods, np.random.permutation(self.cities))
        self.sa_search(start_temp, maxIter,alpha)

    def sa_search(self, temp, maxIter, alpha):
        candidate = self.saBest
        for i in range(maxIter):
            n_hood = self.getNeighborhood(candidate)
            random_neighbor = random.choice(n_hood)
            if random_neighbor.cost < candidate.cost or random.random() <= np.exp(-(random_neighbor.cost[0] - candidate.cost[0])/temp):
                candidate = random_neighbor
            if candidate.cost < self.saBest.cost:
                self.saBest = candidate
                print("Improvement Found!")
                print("Iteration: ", i, "\nBest")
                print(self.saBest)
            temp = temp*alpha


    def getNeighborhood(self, candidate):
        neighborhood = []
        for i in range(len(candidate.config)):
            for j in range(i + 1, len(candidate.config)):
                new_node = [i for i in candidate.config]
                new_node[i], new_node[j] = new_node[j], new_node[i]
                neighborhood.append(
                    VRP(self.truck_capacity, self.city_dist_matrix, self.goods, np.array(new_node)))
        return neighborhood
