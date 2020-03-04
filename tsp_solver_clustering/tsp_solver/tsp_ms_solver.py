from operator import itemgetter

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth

from tsp_solver_clustering.genetic_algorithm.city import City
from tsp_solver_clustering.plots.plots import plot_ms_results
from tsp_solver_clustering.reading_example_problems.tsp import TspSubproblem
from tsp_solver_clustering.tsp_solver.tsp_af_solver import (
    solve_and_merge_subproblems_naive,
)


def solve_mean_shift(tsp_problem, plot=False):
    """ Solves TSP problem using mean shift clustering

    :param tsp_problem: Tsp
    :param plot: Yes/No plotting
    :return: best route
    """
    # Convert cities to nd array
    matrix_x = []
    for city in tsp_problem.cities:
        matrix_x.append([city.x, city.y])
    matrix_x = np.array(matrix_x)

    # Mean shift clustering
    bandwidth = estimate_bandwidth(matrix_x, quantile=0.2, n_samples=500)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(matrix_x)

    cluster_centers = ms.cluster_centers_
    labels = ms.labels_
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    # Plotting the results
    if plot:
        plot_ms_results(matrix_x, n_clusters_, labels, cluster_centers)

    # Define the subproblems
    subproblems = []
    for i in range(n_clusters_):
        indecies = [a for a, x in enumerate(labels) if x == i]
        if len(indecies) == 1:
            cities_in_subproblem = [tsp_problem.cities[indecies[0]]]
        else:
            cities_in_subproblem = list(itemgetter(*indecies)(tsp_problem.cities))
        subproblem_center = City(
            id="center", x=cluster_centers[i][0], y=cluster_centers[i][1]
        )
        subproblems.append(
            TspSubproblem(
                name=tsp_problem.name + "_" + str(i),
                cities=cities_in_subproblem,
                center=subproblem_center,
            )
        )

    # Solve and merge subproblems
    best_route = solve_and_merge_subproblems_naive(subproblems, plot)

    return best_route
