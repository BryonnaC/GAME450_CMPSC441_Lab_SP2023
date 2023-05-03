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
import math

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

    #okay what if for the distribution, I just copy cities into a new list and compare that way?
    cities_copy = cities

    for city in cities:
        # check if city location is underwater
        # print(elevation[[city[0]],city[1]]) #okay okay, now we got it

        # This set of if/else checks to see whether the city's elevation
        # is below .4. This is assuming that .4 and below are under water, in water, or too close to water.
        if(elevation[[city[0]],city[1]] < .4):
            fitness -= 2
        else:
            fitness += 1

        # This set of if/else checks to see whether the city's elevation
        # is above .7. If it's above .7 it is likely too high elevation.
        if(elevation[[city[0]],city[1]] > .7):
            fitness -= 2
        else:
            fitness += 1

        # This for loop uses the copied list of cities to compare each city by each other city
        for city_copy in cities_copy:
            # This first if statement checks to make sure we aren't comparing the city against itself
            if((city[0] == city_copy[0]) and (city[1] == city_copy[1])):
                pass    # they're the same city, would probably want to check the orig list beforehand to make sure no duplicates
                        # but having duplicates is extremely unlikely
                break
            else:
                # Otherwise, we want to get the distance between the two cities using the algebraic distance formula
                distance = math.sqrt(pow(city_copy[0] - city[0], 2) + pow(city_copy[1] - city[1], 2))
                # And then if the distance is less than 1000, it makes the fitness significantly worse
                # This is to stop the cities from being too close
                if(distance < 1000):
                    fitness -= 3
                # If the distance is larger than 1500, the map should have well distributed cities
                if(distance > 1500 and distance < 3000):
                    fitness += 2
                # But we also want to give a smaller bonus for things being too far, far is good but too far is sparse
                if(distance > 3000):
                    fitness += 1
                # If the distance is between 1000 and 1500, it's okay but we don't want the whole map to be like that
                if(distance > 1000 and distance < 1500):
                    fitness += 1
                pass
                # Generally I kept the buffs at 1 so that they would all be weighted equally,
                # but I made the one a value of +2 so that it would be more likely to have a larger impact

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

def psuedo_ga_main(size):
    print("Initial Population")

    #size = 100, 100
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
    #show_cities(cities, landscape_pic)

    # Run the GA to optimize the parameters of the function.
    ga_instance.run()
    #ga_instance.plot_fitness()
    print("Final Population")

    # Show the best solution after the GA finishes running.
    cities = ga_instance.best_solution()[0]
    cities_t = solution_to_cities(cities, size)
    # plt.imshow(landscape_pic, cmap="gist_earth")
    # plt.plot(cities_t[:, 1], cities_t[:, 0], "r.")
    # plt.show()
    print(fitness_function(cities, 0))

    return [elevation, cities_t]

if __name__ == "__main__":
    psuedo_ga_main()
    exit

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
