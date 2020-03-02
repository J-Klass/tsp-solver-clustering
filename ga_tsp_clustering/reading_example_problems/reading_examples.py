import os

from ga_tsp_clustering.genetic_algorithm.city import City
from ga_tsp_clustering.reading_example_problems.tsp import TSP


def read_all_problems():
    # Create empty list of tsp problems
    tsp_problems = []
    # Checking all problems in folder
    directory = "ga_tsp_clustering/example_problems/problems"
    files = os.listdir(directory)
    for file in files:
        if not file[0] == ".":
            problem_name = file.split(".")[0]
            tsp_problems.append(reading_tsp_files(problem_name))
    return tsp_problems


def reading_tsp_files(problem_name):
    # Create paths to files
    path_to_problem_file = (
        "ga_tsp_clustering/example_problems/problems/" + problem_name + ".tsp"
    )
    path_to_solution_file = (
        "ga_tsp_clustering/example_problems/solutions/" + problem_name + ".opt.tour"
    )

    # Reading the problem file
    file = open(path_to_problem_file, "r")
    # Empty list for cities
    cities = []
    for x in file:
        # Reading the problem name
        if x.split()[0] == "NAME":
            tsp_name = x.split()[2]

        # Reading all the cities
        elif x[0].isdigit():
            values = x.split()
            cities.append(City(id=values[0], x=values[1], y=values[2]))

    # Reading the optimal file
    file = open(path_to_solution_file, "r")
    # Empty list for best route
    best_route = []
    for x in file:
        if x[0].isdigit():
            values = x.split()
            best_route.append(values[0])

    # Create tsp object
    return TSP(name=tsp_name, cities=cities, best_route=best_route)
