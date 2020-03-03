import os

from tsp_solver_clustering.genetic_algorithm.city import City
from tsp_solver_clustering.reading_example_problems.tsp import Tsp


def read_all_problems():
    """ Reading all the example problem

    :return: List of tsp problems
    """
    # Create empty list of tsp problems
    tsp_problems = []
    # Checking all problems in folder
    directory = "tsp_solver_clustering/example_problems/problems"
    files = os.listdir(directory)
    for file in files:
        if not file[0] == ".":
            problem_name = file.split(".")[0]
            tsp_problems.append(reading_tsp_files(problem_name))
    return tsp_problems


def reading_tsp_files(problem_name):
    """ Reading and parsing a single tsp file

    :param problem_name: name of the tsp problem
    :return: TSP objects
    """
    # Create paths to files
    path_to_problem_file = (
        "tsp_solver_clustering/example_problems/problems/" + problem_name + ".tsp"
    )
    path_to_solution_file = (
        "tsp_solver_clustering/example_problems/solutions/" + problem_name + ".opt.tour"
    )

    # Reading the problem file
    file = open(path_to_problem_file, "r")
    # Empty list for cities
    cities = []
    tsp_name = ""
    for x in file:
        # Reading the problem name
        if x.split()[0] == "NAME":
            tsp_name = x.split()[2]

        # Reading all the cities
        elif x[0].isdigit():
            values = x.split()
            cities.append(City(id=values[0], x=float(values[1]), y=float(values[2])))

    # Reading the optimal file
    file = open(path_to_solution_file, "r")
    # Empty list for best route
    best_route = []
    for x in file:
        if x[0].isdigit():
            values = x.split()
            best_route.append(values[0])

    # Create tsp object
    return Tsp(name=tsp_name, cities=cities, best_route=best_route)
