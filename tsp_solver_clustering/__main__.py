import timeit
from statistics import mean

import pandas as pd
import tqdm

from tsp_solver_clustering.genetic_algorithm.fitness import Fitness
from tsp_solver_clustering.reading_example_problems.reading_examples import (
    read_all_problems,
)
from tsp_solver_clustering.tsp_solver.basic_solve import solve_tsp_basic
from tsp_solver_clustering.tsp_solver.tsp_af_solver import solve_tsp_affinity_propagation


def main():
    run_and_evaluate()


def run_and_evaluate():
    """ Running all the problems and summarizing the results

    :return: DataFrame of results
    """
    tsp_problems = read_all_problems()
    # Empty list of metrics
    results = []
    for problem in tqdm.tqdm(tsp_problems):
        # As random factors are involved repeat experiments a couple of times
        best_routes_base = []
        best_routes_af = []
        base_times = []
        af_times = []
        for i in range(10):
            # Base solution
            start_time = timeit.default_timer()
            best_route_base = solve_tsp_basic(problem)
            base_time = timeit.default_timer() - start_time
            best_routes_base.append(Fitness(route=best_route_base).route_distance())
            base_times.append(base_time)

            # AF clustering solution
            start_time = timeit.default_timer()
            best_route_af = solve_tsp_affinity_propagation(problem)
            af_time = timeit.default_timer() - start_time
            best_routes_af.append(Fitness(route=best_route_af).route_distance())
            af_times.append(af_time)

        results.append(
            {
                "problem name": problem.name,
                "optimal solution": find_route_optimal_route_length(problem),
                "baseline tour length": mean(best_routes_base),
                "clustering tour length": mean(best_routes_af),
                "baseline algorithm time": mean(base_times),
                "clustering algorithm time": mean(af_times),
            }
        )
    # Create dataframe and safe results
    df = pd.DataFrame(results)
    df.to_csv("results.csv", index=False)
    return df


def find_route_optimal_route_length(tsp):
    """ Finds the best route length of a problem

    :param tsp: Tsp
    :return: optimal tour length
    """
    best_route = []
    for city_id in tsp.best_route:
        for city in tsp.cities:
            if city_id == city.id:
                best_route.append(city)
    return Fitness(route=best_route).route_distance()


if __name__ == "__main__":
    main()
