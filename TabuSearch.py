from MetaHeuristicFramework import VRP
import numpy as np
import random
import time


class TabuSearch:
    def __init__(self, capacity, dist_matrix, goods, maxTabuSize=100000, search_time=120, output=False):
        self.tabu_list = {}
        self.cities = list(range(1, len(goods)))
        self.city_dist_matrix = dist_matrix
        self.goods = goods
        self.truck_capacity = capacity
        self.tsBest = VRP(capacity, dist_matrix, goods)
        self.tabu_list[self.tsBest.config.tobytes()] = 0
        self.t_search(search_time, maxTabuSize, output)

    def t_search(self,  search_time, t_size, output):
        best_candidate = self.tsBest
        last_improved = 1
        end_time = time.time() + search_time
        time_left = end_time - time.time()
        while time_left > 0:
            neighborhood = self.getNeighborhood(best_candidate)
            best_candidate = None
            for cand in neighborhood:
                if self.tabu_list.get(cand.config.tobytes()) is None and (best_candidate is None or best_candidate.cost[0] > cand.cost[0]):
                    best_candidate = cand
            if best_candidate.cost[0] < self.tsBest.cost[0]:
                if output:
                    self.tsBest = VRP(self.truck_capacity, self.city_dist_matrix, self.goods, config=best_candidate.config.copy())
                    print("Improvement Found!")
                    print("Best:")
                    print(self.tsBest)
                last_improved = 1
            else:
                last_improved += 1
            self.tabu_list[best_candidate.config.tobytes()] = 0
            for tenure in self.tabu_list.keys():
                self.tabu_list[tenure] += 1
            if len(self.tabu_list) > t_size:
                key_to_delete = max(self.tabu_list, key=lambda k: self.tabu_list[k])
                del self.tabu_list[key_to_delete]
            if not last_improved % 100:
                if output:
                    print("Mutation ")
                best_candidate = self.mutate()
            if last_improved == 300:
                if output:
                    print("Random Reset")
                city_list = self.cities.copy()
                best_candidate = VRP(self.truck_capacity, self.city_dist_matrix, self.goods, config=random.shuffle(city_list))
                last_improved = 0
            time_left = end_time - time.time()

    def __str__(self):
        string = "Tabu Search:\nThe Best Route Found: \n"
        return string + str(self.tsBest)

    def getNeighborhood(self, candidate):
        neighborhood = []
        for i in range(len(candidate.config)):
            for j in range(i+1, len(candidate.config)):
                new_node = [i for i in candidate.config]
                new_node[i], new_node[j] = new_node[j], new_node[i]
                neighborhood.append(VRP(self.truck_capacity, self.city_dist_matrix, self.goods, np.array(new_node)))
        return neighborhood

    def mutate(self):
        while True:
            s_points = random.sample(range(len(self.tsBest.config)), 2)
            s_points.sort()
            start, end = s_points[0], s_points[1]
            part = self.tsBest.config[start:end].copy()
            random.shuffle(part)
            new_config = self.tsBest.config.copy()
            new_config[start:end] = part
            best_candidate = VRP(self.truck_capacity, self.city_dist_matrix, self.goods, new_config)
            if self.tabu_list.get(best_candidate.config.tobytes()) is None:
                return best_candidate
