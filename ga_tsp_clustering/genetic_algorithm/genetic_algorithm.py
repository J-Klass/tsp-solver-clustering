import operator
import random

import numpy as np
import pandas as pd

from ga_tsp_clustering.genetic_algorithm.fitness import Fitness
from ga_tsp_clustering.plots.plots import plot_progress


def create_route(city_list):
    """ Creates an initial route for the cities
    :param city_list: list of cities
    :return: randomly generated route
    """
    route = random.sample(city_list, len(city_list))
    return route


def initial_population(pop_size, city_list):
    """ Creates an initial population
    :param pop_size: size of the population
    :param city_list: list of cities
    :return: population (list of queen placements)
    """
    population = []

    for i in range(0, pop_size):
        population.append(create_route(city_list))
    return population


def rank_routes(population):
    """ Rank individuals
    :param population: population
    :return: sorted population
    """
    fitness_results = {}
    for i in range(0, len(population)):
        fitness_results[i] = Fitness(population[i]).route_fitness()
    return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)


def selection(pop_ranked, elite_size):
    """ Selection function to create list of parent routes
    :param pop_ranked: ranked population
    :param elite_size: size of the elite
    :return: selected routes out of the population
    """
    selection_results = []
    df = pd.DataFrame(np.array(pop_ranked), columns=["Index", "Fitness"])
    df["cum_sum"] = df.Fitness.cumsum()
    df["cum_perc"] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, elite_size):
        selection_results.append(pop_ranked[i][0])
    for i in range(0, len(pop_ranked) - elite_size):
        pick = 100 * random.random()
        for i in range(0, len(pop_ranked)):
            if pick <= df.iat[i, 3]:
                selection_results.append(pop_ranked[i][0])
                break
    return selection_results


def mating_pool(population, selection_results):
    """ Creating a mating pool
    :param population: population
    :param selection_results: selected individuals from population
    :return: mating pool
    """
    matingpool = []
    for i in range(0, len(selection_results)):
        index = selection_results[i]
        matingpool.append(population[index])
    return matingpool


def breed(parent_1, parent_2):
    """ A crossover function for two parents to create one child
    :param parent_1: parent 1
    :param parent_2: parent 2
    :return: child route
    """
    child = []
    child_p1 = []
    child_p2 = []

    gene_a = int(random.random() * len(parent_1))
    gene_b = int(random.random() * len(parent_1))

    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)

    for i in range(start_gene, end_gene):
        child_p1.append(parent_1[i])

    child_p2 = [item for item in parent_2 if item not in child_p1]

    child = child_p1 + child_p2
    return child


def breed_population(matingpool, elite_size):
    """ Function to run crossover over full mating pool
    :param matingpool: mating pool
    :param elite_size: size of elite individuals
    :return: children
    """
    children = []
    length = len(matingpool) - elite_size
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0, elite_size):
        children.append(matingpool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])
        children.append(child)
    return children


def mutate(individual, mutation_rate):
    """ Function to mutate an individual
    :param individual: individual i.e. single placement
    :param mutation_rate: rate of mutations
    :return: individual
    """
    for swapped in range(len(individual)):
        if random.random() < mutation_rate:
            swap_with = int(random.random() * len(individual))

            queen_1 = individual[swapped]
            queen_2 = individual[swap_with]

            individual[swapped] = queen_2
            individual[swap_with] = queen_1
    return individual


def mutate_population(population, mutation_rate):
    """ Run mutation on entire population
    :param population: population of routes
    :param mutation_rate: rate of mutations
    :return: mutated population
    """

    mutated_pop = []

    for ind in range(0, len(population)):
        mutated_ind = mutate(population[ind], mutation_rate)
        mutated_pop.append(mutated_ind)
    return mutated_pop


def next_generation(current_gen, elite_size, mutation_rate):
    """ Combination of steps to create next generation
    :param current_gen: current generation
    :param elite_size: size of elite individuals
    :param mutation_rate: rate of mutation
    :return: next generation
    """
    pop_ranked = rank_routes(current_gen)
    selection_results = selection(pop_ranked, elite_size)
    matingpool = mating_pool(current_gen, selection_results)
    children = breed_population(matingpool, elite_size)
    next_generation = mutate_population(children, mutation_rate)
    return next_generation


def genetic_algorithm(
    population, pop_size, elite_size, mutation_rate, generations, plot=False
):
    """ Complete genetic algorithm
    :param population: population
    :param pop_size: size of population
    :param elite_size: size of elite
    :param mutation_rate: rate of mutation
    :param generations: number of generations
    :param plot: plotting yes/no
    :return: best individual
    """
    pop = initial_population(pop_size, population)
    progress = []
    progress.append(1 / rank_routes(pop)[0][1])

    for i in range(0, generations):
        pop = next_generation(pop, elite_size, mutation_rate)
        progress.append(1 / rank_routes(pop)[0][1])

    if plot:
        plot_progress(progress)
    best_route_index = rank_routes(pop)[0][0]
    best_route = pop[best_route_index]
    return best_route
