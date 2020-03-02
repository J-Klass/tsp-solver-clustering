from ga_tsp_clustering.reading_example_problems.reading_examples import read_all_problems


def main():
    # Reading and solving all problems
    tsp_problems = read_all_problems()
    print(tsp_problems)


if __name__ == "__main__":
    main()
