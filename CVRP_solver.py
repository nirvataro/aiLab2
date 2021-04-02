from sys import argv
<<<<<<< Updated upstream
import MetaHeuristicFramework as mhf


def cvrp(vehicles, capacity, dist_matrix, goods):
    solution = mhf.find_solution()
    pass
=======
import numpy as np
from scipy.spatial import distance
from TabuSearch import TabuSearch
from SimulatedAnnealing import SimulatedAnnealing
from AntColonyOptimization import AntColonyOpt


def cvrp(capacity, dist_matrix, goods):
    print(AntColonyOpt(capacity, dist_matrix, goods))
>>>>>>> Stashed changes


def config_data(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    for l in lines:
        l.strip()

    return vehicles, capacity, dist_matrix, goods


if __name__ == '__main__':
<<<<<<< Updated upstream
    input_file = argv[1]
    vehicles, capacity, dist_matrix, goods = config_data(input_file)
    cvrp(vehicles, capacity, dist_matrix, goods)
=======
    input_file = 'E-n33-k4.txt'   # argv[1]
    capacity, dist_matrix, goods = config_data(input_file)
    cvrp(capacity, dist_matrix, goods)
>>>>>>> Stashed changes
