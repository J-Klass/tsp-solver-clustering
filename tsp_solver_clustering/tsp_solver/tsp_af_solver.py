import itertools
import multiprocessing
from operator import itemgetter

import numpy as np
from joblib import Parallel, delayed
from sklearn.cluster import AffinityPropagation

from tsp_solver_clustering.genetic_algorithm.genetic_algorithm import genetic_algorithm
from tsp_solver_clustering.plots.plots import plot_af_clustering_results, plot_route
from tsp_solver_clustering.reading_example_problems.tsp import TspSubproblem


def solve_tsp_affinity_propagation(tsp_problem, plot=False):
    """ Solves TSP problem using affinity propagation clustering

    :param tsp_problem: Tsp
    :param plot: Yes/No plotting
    :return: best route
    """
    # Convert cities to nd array
    matrix_x = []
    for city in tsp_problem.cities:
        matrix_x.append([city.x, city.y])
    matrix_x = np.array(matrix_x)

    # Affinity propagation clustering
    af = AffinityPropagation().fit(matrix_x)
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_
    n_clusters_ = len(cluster_centers_indices)
    # Plotting the results
    if plot:
        plot_af_clustering_results(matrix_x, n_clusters_, labels, cluster_centers_indices)

    # Define the subproblems
    subproblems = []
    for i in range(n_clusters_):
        indecies = [a for a, x in enumerate(labels) if x == i]
        cities_in_subproblem = list(itemgetter(*indecies)(tsp_problem.cities))
        subproblem_center = tsp_problem.cities[cluster_centers_indices[i]]
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


def solve_and_merge_subproblems_naive(subproblems, plot):
    """ Solving and merging the subproblems in parallel

    :param subproblems: Subproblem
    :param plot: yes/no plotting
    :return: best route
    """
    # Find the shortest route connecting the centers
    centers = []
    for subproblem in subproblems:
        centers.append(subproblem.center)
    best_route_centers = genetic_algorithm(
        population=centers,
        pop_size=100,
        elite_size=20,
        mutation_rate=0.01,
        generations=10,
    )
    # Plotting the best route to connect the centers
    if plot:
        plot_route(best_route_centers)

    # Adding multiprocessing
    num_cores = multiprocessing.cpu_count()
    # Find the best solutions in parallel in the subproblems and connect them
    best_route = Parallel(n_jobs=num_cores)(
        delayed(solve_subproblem)(i, subproblems) for i in best_route_centers
    )
    best_route = list(itertools.chain(*best_route))
    return best_route


def solve_subproblem(center_city, subproblems):
    """Finds the solution of a subproblem

    :param center_city: Id of the city in the center
    :param subproblems: List of subproblems
    :return: best route
    """
    best_sub_route = []
    tsp_subproblem = next((x for x in subproblems if x.center == center_city), None)
    if not len(tsp_subproblem.cities) == 1:
        best_sub_route.extend(
            genetic_algorithm(
                population=tsp_subproblem.cities,
                pop_size=100,
                elite_size=20,
                mutation_rate=0.01,
                generations=50,
            )
        )
    else:
        best_sub_route.extend(tsp_subproblem.cities)
    return best_sub_route
