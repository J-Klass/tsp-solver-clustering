import timeit

import pandas as pd

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
    for problem in tsp_problems:
        # Base solution
        start_time = timeit.default_timer()
        best_route_base = solve_tsp_basic(problem)
        base_time = timeit.default_timer() - start_time

        # AF clustering solution
        start_time = timeit.default_timer()
        best_route_af = solve_tsp_affinity_propagation(problem)
        af_time = timeit.default_timer() - start_time

        results.append(
            {
                "problem name": problem.name,
                "baseline algorithm time": base_time,
                "baseline tour length": Fitness(route=best_route_base).route_distance(),
                "clustering algorithm time": af_time,
                "clustering tour length": Fitness(route=best_route_af).route_distance(),
            }
        )
    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    main()
