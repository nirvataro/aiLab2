from sys import argv
import MetaHeuristicFramework as mhf


def cvrp(vehicles, capacity, dist_matrix, goods):
    solution = mhf.find_solution()
    pass


def config_data(input_file):

    return vehicles, capacity, dist_matrix, goods


if __name__ == '__main__':
    input_file = argv[1]
    vehicles, capacity, dist_matrix, goods = config_data(input_file)
    cvrp(vehicles, capacity, dist_matrix, goods)