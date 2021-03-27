from MetaHeuristicFramework import VRP, Truck


class TabuSearch(VRP):
    def __init__(self, capacity, dist_matrix, goods):
        super().__init__(capacity, dist_matrix, goods)
        self.tabu_list = []





