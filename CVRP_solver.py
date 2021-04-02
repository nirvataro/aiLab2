from sys import argv
import numpy as np
from scipy.spatial import distance
from TabuSearch import TabuSearch
from SimulatedAnnealing import SimulatedAnnealing
from AntColonyOptimization import AntColonyOpt

def cvrp(capacity, dist_matrix, goods):
    print(TabuSearch(capacity, dist_matrix, goods))

    
def config_data(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    for l in lines:
        l.strip()
    coords, goods = [], []
    for idx, l in enumerate(lines):
        if l.startswith('DIMENSION :'):
            l = l.replace('DIMENSION : ', '')
            dim = int(l)
        if l.startswith("CAPACITY : "):
            l = l.replace('CAPACITY : ', '')
            capacity = int(l)
        if l.startswith('NODE_COORD_SECTION'):
            for i in range(idx+1, dim+idx+1):
                p = lines[i].split()
                coords.append((int(p[1]), int(p[2])))
        if l.startswith('DEMAND_SECTION'):
            for i in range(idx + 1, dim + idx + 1):
                g = lines[i].split()
                goods.append(int(g[1]))
    dist_matrix = np.array([[0 for _ in range(dim)] for _ in range(dim)], float)
    for index_i, cord_i in enumerate(coords):
        for index_j, cord_j in enumerate(coords):
            dist_matrix[index_i][index_j] = distance.euclidean(cord_i, cord_j)
    return capacity, dist_matrix, goods


if __name__ == '__main__':
#     input_file = 'E-n33-k4.txt'   # argv[1]
#     capacity, dist_matrix, goods = config_data(input_file)
#     cvrp(capacity, dist_matrix, goods)

    input_file = 'E-n22-k4.txt'   # argv[1]
    capacity, dist_matrix, goods = config_data(input_file)
    cvrp(capacity, dist_matrix, goods)
