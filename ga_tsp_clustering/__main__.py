from ga_tsp_clustering.reading_example_problems.reading_examples import read_all_problems
from ga_tsp_clustering.tsp_solver.basic_solve import solve_tsp_basic


def main():
    # Reading and solving all problems
    tsp_problem = read_all_problems()
    for problem in tsp_problem:
        print(problem.name)
        print("GA found solution: ")
        print(solve_tsp_basic(problem))
        print("Actual best solution")
        print(problem.best_route)


if __name__ == "__main__":
    main()
