from tsp_solver_clustering.plots.plots import plot_problem, plot_route
from tsp_solver_clustering.reading_example_problems.reading_examples import (
    read_all_problems,
)
from tsp_solver_clustering.tsp_solver.tsp_af_solver import solve_tsp_affinity_propagation


def main():
    # Reading an example problem
    tsp_problems = read_all_problems()
    # Plot the problem
    plot_problem(tsp_problems[1])
    # Solve the problem using clustering and plot the result
    plot_route(solve_tsp_affinity_propagation(tsp_problems[1]))


if __name__ == "__main__":
    main()
