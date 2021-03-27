from MetaHeuristicFramework import VRP
import numpy as np
import pandas as pd


class TabuSearch:
    def __init__(self, capacity, dist_matrix, goods, maxTabuSize = 10000, maxIter = 10000):
        self.tabu_list = []
        unvisited_cities = list(range(1, len(goods)))
        self.sBest = VRP(capacity, dist_matrix, goods, np.random.permutation(unvisited_cities))
        self.best_candidate = self.sBest
        self.tabu_list.append(np.array(self.sBest.config))
        for i in range(maxIter):
            neighborhood = self.getNeighborhood()
            self.best_candidate = VRP(capacity, dist_matrix, goods, neighborhood[0])
            for con in neighborhood:
                temp_con = VRP(capacity, dist_matrix, goods, con)
                a = np.asarray(self.tabu_list)
                if (not np.all(np.isclose(a, temp_con.config))) and (temp_con.cost < self.best_candidate.cost):
                    self.best_candidate = temp_con
            if self.sBest.cost > self.best_candidate.cost:
                self.sBest = self.best_candidate
            self.tabu_list.append(np.array(self.best_candidate.config))
            if len(self.tabu_list) > maxTabuSize:
                del self.tabu_list[0]
            print(self.__getattr__())

    def __getattr__(self):
        routes = []
        for t in self.sBest.trucks:
            routes.append(t.route)
        return routes, self.sBest.cost

    def getNeighborhood(self):
        neighborhood = []
        for i in range(len(self.best_candidate.config)):
            for j in range(i+1, len(self.best_candidate.config)):
                new_node = [i for i in self.best_candidate.config]
                new_node[i], new_node[j] = new_node[j], new_node[i]
                neighborhood.append(new_node)
        return neighborhood
