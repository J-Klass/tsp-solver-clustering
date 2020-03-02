from ga_tsp_clustering.reading_example_problems.reading_examples import read_all_problems


def main():
    # Reading and printing all problems
    tsp_problem = read_all_problems()
    for problem in tsp_problem:
        print(problem.name)


if __name__ == "__main__":
    main()
