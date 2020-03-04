from itertools import cycle

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


def plot_af_clustering_results(X, n_clusters_, labels, cluster_centers_indices):
    """ Plotting the results of affinity propagation clustering

    :param X: Matrix
    :param n_clusters_: number of clusters
    :param labels: cluster label
    :param cluster_centers_indices: centers
    :return: none
    """
    plt.close("all")
    plt.figure(1)
    plt.clf()

    colors = cycle("bgrcmykbgrcmykbgrcmykbgrcmyk")
    for k, col in zip(range(n_clusters_), colors):
        class_members = labels == k
        cluster_center = X[cluster_centers_indices[k]]
        plt.plot(X[class_members, 0], X[class_members, 1], col + ".")
        plt.plot(
            cluster_center[0],
            cluster_center[1],
            "o",
            markerfacecolor=col,
            markeredgecolor="k",
            markersize=14,
        )
        for x in X[class_members]:
            plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

    plt.title("Estimated number of clusters: %d" % n_clusters_)
    plt.show()


def plot_ms_results(X, n_clusters_, labels, cluster_centers):
    """ Plotting the results of the mean shift clustering algorithm

    :param X: Matrix of points
    :param n_clusters_: number of clusters
    :param labels: labels of clusters
    :param cluster_centers: coordinates of cluster centers
    :return: none
    """
    plt.figure(1)
    plt.clf()

    colors = cycle("bgrcmykbgrcmykbgrcmykbgrcmyk")
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], col + ".")
        plt.plot(
            cluster_center[0],
            cluster_center[1],
            "o",
            markerfacecolor=col,
            markeredgecolor="k",
            markersize=14,
        )
    plt.title("Estimated number of clusters: %d" % n_clusters_)
    plt.show()
