"""
Lab 7: Realistic Cities 

In this lab you will try to generate realistic cities using a genetic algorithm.
Your cities should not be under water, and should have a realistic distribution across the landscape.
Your cities may also not be on top of mountains or on top of each other.
Create the fitness function for your genetic algorithm, so that it fulfills these criterion
and then use it to generate a population of cities. #recommend implementing one criteria for now, then go from there

Please comment your code in the fitness function to explain how are you making sure each criterion is 
fulfilled. Clearly explain in comments which line of code and variables are used to fulfill each criterion.
"""
import matplotlib.pyplot as plt
import pygad
import numpy as np

import sys
from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / ".." / "..").resolve().absolute()))

from src.lab5.landscape import elevation_to_rgba, get_elevation, get_landscape


def game_fitness(cities, idx, elevation, size):
    fitness = 0.0001  # Do not return a fitness of 0, it will mess up the algorithm.
    """
    Create your fitness function here to fulfill the following criteria:
    1. The cities should not be under water
    2. The cities should have a realistic distribution across the landscape
    3. The cities may also not be on top of mountains or on top of each other
    """
    # okay so make citites back into coordinates
    cities = solution_to_cities(cities, size)

    #cities should not be underwater - elevation
    # okay so we want to check if a city is underwater? and then move it?
    # cities is an array of the cities
    # elevation is an array of length 10000, so it has an elevation for every possible coord on the 100x100 map
    for city in cities:
        # check if city location is underwater
        #print(elevation[[city[0]],city[1]]) #okay okay, now we got it

        # water elevation and below? .3 is just a guess
        if(elevation[[city[0]],city[1]] < .4):
            #move the city? idk - move it by how much??? - this doesn't make any sense lmao
            # I don't think I have to move the city, I just have to change fitness?
            fitness -= 2
        else:
            fitness += .5

        #on a big boi mountain top? not allowed
        if(elevation[[city[0]],city[1]] > .7):
            fitness -= 1
        else:
            fitness += 1

    return fitness


def setup_GA(fitness_fn, n_cities, size):
    """
    It sets up the genetic algorithm with the given fitness function,
    number of cities, and size of the map

    :param fitness_fn: The fitness function to be used
    :param n_cities: The number of cities in the problem
    :param size: The size of the grid
    :return: The fitness function and the GA instance.
    """
    num_generations = 100
    num_parents_mating = 10

    solutions_per_population = 300
    num_genes = n_cities

    init_range_low = 0
    init_range_high = size[0] * size[1]

    #don't need to change any of the pygad params, but we can b/c its a sandbox
    parent_selection_type = "sss"
    keep_parents = 10

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_fn,
        sol_per_pop=solutions_per_population,
        num_genes=num_genes,
        gene_type=int,
        init_range_low=init_range_low,
        init_range_high=init_range_high,
        parent_selection_type=parent_selection_type,
        keep_parents=keep_parents,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes,
    )

    return fitness_fn, ga_instance


def solution_to_cities(solution, size):
    """
    It takes a GA solution and size of the map, and returns the city coordinates
    in the solution.

    :param solution: a solution to GA
    :param size: the size of the grid/map
    :return: The cities are being returned as a list of lists.
    """
    cities = np.array(
        list(map(lambda x: [int(x / size[0]), int(x % size[1])], solution))
    ) # for each int x we create a list/array which is all of the cities and their coordinates - solution is pixel loc of city (count of pixels away from top left)
    return cities


def show_cities(cities, landscape_pic, cmap="gist_earth"):
    """
    It takes a list of cities and a landscape picture, and plots the cities on top of the landscape

    :param cities: a list of (x, y) tuples
    :param landscape_pic: a 2D array of the landscape
    :param cmap: the color map to use for the landscape picture, defaults to gist_earth (optional)
    """
    cities = np.array(cities)
    plt.imshow(landscape_pic, cmap=cmap)
    plt.plot(cities[:, 1], cities[:, 0], "r.")
    plt.show()


if __name__ == "__main__":
    print("Initial Population")

    size = 100, 100
    n_cities = 10
    elevation = []
    #""" initialize elevation here from your previous code"""
    elevation = get_elevation(size)
    # normalize landscape
    elevation = np.array(elevation)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())
    landscape_pic = elevation_to_rgba(elevation)

    # setup fitness function and GA
    fitness = lambda cities, idx: game_fitness(
        cities, idx, elevation=elevation, size=size
    )
    fitness_function, ga_instance = setup_GA(fitness, n_cities, size)

    # Show one of the initial solutions.
    cities = ga_instance.initial_population[0]
    cities = solution_to_cities(cities, size)
    show_cities(cities, landscape_pic)

    # Run the GA to optimize the parameters of the function.
    ga_instance.run()
    ga_instance.plot_fitness()
    print("Final Population")

    # Show the best solution after the GA finishes running.
    cities = ga_instance.best_solution()[0]
    cities_t = solution_to_cities(cities, size)
    plt.imshow(landscape_pic, cmap="gist_earth")
    plt.plot(cities_t[:, 1], cities_t[:, 0], "r.")
    plt.show()
    print(fitness_function(cities, 0))
