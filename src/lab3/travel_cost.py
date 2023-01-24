'''
Lab 3: Travel Cost

Your player will need to move from one city to another in order to complete the game.
The player will have to spend money to travel between cities. The cost of travel depends 
on the difficulty of the terrain.
In this lab, you will write a function that calculates the cost of a route between two cities,
A terrain is generated for you 
'''
import numpy as np

def get_route_cost(route_coordinate, game_map):
    """
    This function takes in a route_coordinate as a tuple of coordinates of cities to connect, 
    example:  and a game_map as a numpy array of floats,
    remember from previous lab the routes looked like this: [(A, B), (A, C)]
    route_coordinates is just inserts the coordinates of the cities into a route like (A, C).
    route_coordinate might look like this: ((0, 0), (5, 4))

    For each route this finds the cells that lie on the line between the
    two cities at the end points of a route, and then sums the cost of those cells
      -------------
    1 | A |   |   |
      |-----------|
    2 |   |   |   |
      |-----------|
    3 |   | C |   |
      -------------
        I   J   K 

    Cost between cities A and C is the sum of the costs of the cells 
        I1, I2, J2 and J3.
    Alternatively you could use a direct path from A to C that uses diagonal movement, like
        I1, J2, J3

    :param route_coordinates: a list of tuples of coordinates of cities to connect
    :param game_map: a numpy array of floats representing the cost of each cell

    :return: a floating point number representing the cost of the route
    """
    # Build a path from start to end that looks like [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 4)]

    # Get the two cities coordinates
    city_one = route_coordinate[0]
    city_two = route_coordinate[1]

    # Split the tuples into individual coordinates 
    city_one_x = city_one[0]
    city_one_y = city_one[1]
    city_two_x = city_two[0]
    city_two_y = city_two[1]
    
    # We want to go diagonal in the X direction according to lab instructions
    # So compare the x's of city one and city two
    x_diff = city_two_x - city_one_x
    # but now we also need to check y so that we know if we're going up or down
    y_diff = city_one_y - city_two_y
    # TODO consider negative vs positive values (left v right)

    # Create the new list - looks like it should be named path
    path = [ ]
    # x_diff is the number of times that the player needs to move diagonal
    global working_y  # might not need global? unsure, can test
    global working_x  # just need it to hold outside of for loop

    working_x = city_one_x
    working_y = city_one_y

    # Check whether |y_diff| >= |x_diff|
    y_abs = 0
    x_abs = 0

    if(y_diff > 0):
      y_abs = y_diff
    if(y_diff < 0):
      y_abs = -y_diff
    if(x_diff > 0):
      x_abs = x_diff
    if(x_diff < 0):
      x_abs = -x_diff

    # What if x_diff is equal to zero
    if(x_diff == 0):
      diag_moves = 0 # right? but does this case matter? yes - it should probably get checked before all others
    else:
      if( y_abs < x_abs):
        # Need the different of y_abs and x_abs
        diag_moves = x_abs - y_abs
      # Otherwise, there is equal or more movement in the y dir as is in x dir
      if(y_abs >= x_abs):
        diag_moves = x_diff
      # Here we're finally figuring out how many diagonals to do
      for i in range(1, diag_moves-1): # Change*d* this to diag_moves, but does that mess with my neg/pos? probably
        if(x_diff > 0):              # no, actually, I think  if I keep these if compares the same, it'll probably work out.
          working_x += 1
        if(x_diff < 0):
          working_x -= 1
        if(y_diff > 0):
          working_y += 1
        if(y_diff < 0):
          working_y -= 1
        # Now add the tuple to the list
        path_item = (working_x,working_y)
        path.append(path_item)

    # Now we need to figure out if there's any more movements (x or y)
    remain_moves = 0
    if(x_abs > y_abs):
      # We need to do this many more x movements
      remain_moves = x_abs - y_abs
    if(y_abs > x_abs):
      # We need to do this many more y movements
      remain_moves = y_abs - x_abs

    # TODO make the for loop into a function, seems to be reused quite often
    for j in range(1, remain_moves-1):
      # TODO this is not optimal
      if(x_abs > y_abs):
        if(x_diff > 0):              
          working_x += 1
        if(x_diff < 0):
          working_x -= 1
        # Combine with last known working_y
        path_item = (working_x,working_y)
        path.append(path_item)        # TODO ultra repetitive code 
      
      if(y_abs > x_abs):
        if(y_diff > 0):
          working_y += 1
        if(y_diff < 0):
          working_y -= 1
        # Combine with last known working_x
        path_item = (working_x,working_y)
        path.append(path_item)        # TODO ultra repetitive code 

    #pass 
    return game_map[tuple(zip(*path))].sum()


def route_to_coordinates(city_locations, city_names, routes):
    """ get coordinates of each of the routes from cities and city_names"""
    route_coordinates = []
    for route in routes:
        start = city_names.index(route[0])
        end = city_names.index(route[1])
        route_coordinates.append((city_locations[start], city_locations[end]))
    return route_coordinates


def generate_terrain(map_size):
    """ generate a terrain map of size map_size """
    return np.random.rand(*map_size)


def main():
    # Ignore the following 4 lines. This is bad practice, but it's just to make the code work in the lab.
    import sys
    from pathlib import Path
    sys.path.append(str((Path(__file__)/'..'/'..').resolve().absolute()))
    from lab2.cities_n_routes import get_randomly_spread_cities, get_routes

    city_names = ['Morkomasto', 'Morathrad', 'Eregailin', 'Corathrad', 'Eregarta', 
                  'Numensari', 'Rhunkadi', 'Londathrad', 'Baernlad', 'Forthyr']
    map_size = 300, 200

    n_cities = len(city_names)
    game_map = generate_terrain(map_size)
    print(f'Map size: {game_map.shape}')

    city_locations = get_randomly_spread_cities(map_size, n_cities)
    routes = get_routes(city_names)
    np.random.shuffle(routes)
    routes = routes[:10]
    route_coordinates = route_to_coordinates(city_locations, city_names, routes)

    for route, route_coordinate in zip(routes, route_coordinates):
        print(f'Cost between {route[0]} and {route[1]}: {get_route_cost(route_coordinate, game_map)}')


if __name__ == '__main__':
    main()