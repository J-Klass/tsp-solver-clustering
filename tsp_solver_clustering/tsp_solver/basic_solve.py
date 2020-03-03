from tsp_solver_clustering.genetic_algorithm.genetic_algorithm import genetic_algorithm


def solve_tsp_basic(tsp_problem):
    """ Calculates the best solution for a tsp probelm

    :param tsp_problem: TSP problem
    :return: best route
    """
    best_route = genetic_algorithm(
        population=tsp_problem.cities,
        pop_size=100,
        elite_size=20,
        mutation_rate=0.01,
        generations=500,
    )
    return best_route
