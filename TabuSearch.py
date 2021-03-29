from MetaHeuristicFramework import VRP
import numpy as np
import random


class TabuSearch:
    def __init__(self, capacity, dist_matrix, goods, maxTabuSize=100000, maxIter=10000):
        self.tabu_list = {}
        self.cities = list(range(1, len(goods)))
        self.city_dist_matrix = dist_matrix
        self.goods = goods
        self.truck_capacity = capacity
        self.tsBest = VRP(capacity, dist_matrix, goods)
        self.best_candidate = self.tsBest
        self.tabu_list[self.tsBest.config.tobytes()] = 0
        self.t_search(maxIter, maxTabuSize)

    def t_search(self, t_iter, t_size):
        last_improved = 0
        for i in range(t_iter):
            neighborhood = self.getNeighborhood()
            self.best_candidate = None
            for cand in neighborhood:
                if self.tabu_list.get(cand.config.tobytes()) is None and (self.best_candidate is None or self.best_candidate.cost[0] > cand.cost[0]):
                    self.best_candidate = cand
            if self.best_candidate.cost[0] < self.tsBest.cost[0]:
                self.tsBest = self.best_candidate
                print("Improvement Found!")
                print("Iteration: ", i, "\nBest")
                print(self.tsBest)
                last_improved = 0
            else:
                last_improved += 1
            self.tabu_list[self.best_candidate.config.tobytes()] = 0
            for tenure in self.tabu_list.keys():
                self.tabu_list[tenure] += 1
            if len(self.tabu_list) > t_size:
                key_to_delete = max(self.tabu_list, key=lambda k: self.tabu_list[k])
                del self.tabu_list[key_to_delete]
            if not i % 1000 and i > 0:
                print("Iteration: ", i)
                print(self.best_candidate)
            if last_improved == 500:
                print("Random Reset")
                last_improved = 0
                self.perm_mutate()

    def __str__(self):
        string = "Tabu Search:\nThe Best Route Found: \n"
        return string + str(self.tsBest)

    def getNeighborhood(self):
        neighborhood = []
        for i in range(len(self.best_candidate.config)):
            for j in range(i+1, len(self.best_candidate.config)):
                new_node = [i for i in self.best_candidate.config]
                new_node[i], new_node[j] = new_node[j], new_node[i]
                neighborhood.append(VRP(self.truck_capacity, self.city_dist_matrix, self.goods, np.array(new_node)))
        return neighborhood

    def perm_mutate(self):
        while True:
            s_points = random.sample(range(len(self.tsBest.config)), 2)
            s_points.sort()
            start, end = s_points[0], s_points[1]
            part = self.tsBest.config[start:end]
            random.shuffle(part)
            self.best_candidate = self.tsBest
            self.best_candidate.config[start:end] = part
            if self.tabu_list.get(self.best_candidate.config.tobytes()) is None:
                return
