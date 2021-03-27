from MetaHeuristicFramework import VRP, Truck
import numpy as np

class TabuSearch:
    def __init__(self, capacity, dist_matrix, goods, maxIter=10000):
        self.tabu_list = []
        unvisited_citied = list(range(1, len(goods)))
        self.start_config = VRP(capacity, dist_matrix, goods, np.random.permutation(unvisited_citied))
        self.best_canidate = self.start_config
        self.tabu_list.append(self.start_config)
        for i in range(maxIter):
            neighborhood = self.getNeighborhood()
            self.best_canidate = VRP(capacity, dist_matrix, goods, neighborhood[0])
            for con in neighborhood:
                temp_con = VRP(capacity, dist_matrix, goods, con)
                if con not in self.tabu_list and \
                    temp_con.cost < self.best_canidate.cost:
                        self.best_canidate = temp_con



    def getNeighborhood(self):
        neighborhood = []
        for i in range(len(self.best_canidate)):
            for j in range(i, len(self.best_canidate)):
                new_node = self.best_canidate[:]
                new_node[i], new_node[j] = new_node[j], new_node[i]
                neighborhood.append(new_node)
        return neighborhood