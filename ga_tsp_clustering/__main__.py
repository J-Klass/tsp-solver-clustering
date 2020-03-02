import random

from ga_tsp_clustering.genetic_algorithm import genetic_algorithm
from ga_tsp_clustering.genetic_algorithm.city import City


def main():
    # Some sample stuff
    city_list = []
    for i in range(0, 25):
        city_list.append(
            City(x=int(random.random() * 200), y=int(random.random() * 200))
        )
    # Running the algorithm
    best_route = genetic_algorithm.genetic_algorithm(
        population=city_list,
        pop_size=100,
        elite_size=20,
        mutation_rate=0.01,
        generations=500,
    )
    print("The best route is: ", best_route)


if __name__ == "__main__":
    main()