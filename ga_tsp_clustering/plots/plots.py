import matplotlib.pyplot as plt


def plot_progress(progress):
    """ Line plot of the progress over time

    :param progress: progress for each generation
    :return: none
    """
    plt.plot(progress)
    plt.ylabel("Distance")
    plt.xlabel("Generation")
    plt.show()


def plot_problem(tsp_problem):
    """ Simple scatter plot of the problem

    :param tsp_problem: TSP problem
    :return: none
    """
    x = []
    y = []
    labels = []
    for city in tsp_problem.cities:
        x.append(city.x)
        y.append(city.y)
        labels.append(city.id)
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    for i, txt in enumerate(labels):
        ax.annotate(txt, (x[i], y[i]))
    plt.show()


def plot_route(route):
    """ Plot the route in a scatter plot

    :param route: route of all cities
    :return: none
    """
    x = []
    y = []
    labels = []
    for city in route:
        x.append(city.x)
        y.append(city.y)
        labels.append(city.id)
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    for i, txt in enumerate(labels):
        ax.annotate(txt, (x[i], y[i]))
    # Adding first element as last to create cycle
    x.append(x[0])
    y.append(y[0])
    plt.plot(x, y)
    plt.show()
