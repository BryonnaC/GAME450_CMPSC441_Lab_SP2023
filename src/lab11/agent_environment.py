import sys
import pygame
import random
import numpy
from lab11.sprite import Sprite
from lab11.pygame_combat import run_pygame_combat
from lab11.pygame_human_player import PyGameHumanPlayer
from lab11.landscape import get_landscape, get_combat_bg, elevation_to_rgba
from lab11.pygame_ai_player import PyGameAIPlayer

from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab2.cities_n_routes import get_randomly_spread_cities, get_routes
from lab3.travel_cost import get_route_costs
from lab7.ga_cities import psuedo_ga_main
from final_project.image_generator import draw_journal_picture

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)

def get_landscape_surface(size):
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface

def get_landscape_from_elevation(elevation):
    landscape = elevation_to_rgba(elevation)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface

def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])

class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes

def psuedo_agent_environ_main():
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1

    screen = setup_window(width, height, "The Final Game")

    '''use ga here'''
    [elevation, cities] = psuedo_ga_main(size)
    landscape_surface = get_landscape_from_elevation(elevation)

    #landscape_surface = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)
    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    #cities = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:10]

    costs = get_route_costs(cities, city_names, routes, elevation)
    route_list = routes

    player_sprite = Sprite(sprite_path, cities[start_city])

    #start the player with some money
    player = PyGameHumanPlayer(500)

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )

    while True:
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                '''check if route is valid AND if player has enough money'''
                #check if current city and desired city make a valid route
                start = cities[state.current_city]
                state.destination_city = int(chr(action))
                destination = cities[state.destination_city]
                count = 0
                for route in route_list:
                    if route[0][0] == start[0] and route[1][0] == destination[0]:
                    #if [numpy.asarray(start), numpy.asarray(destination)] in routes:
                        route_num = count
                        if costs[route_num] <= player.money:
                            #run turn
                            player_sprite.set_location(cities[state.current_city])
                            player.money -= costs[route_num]
                            state.travelling = True
                            print(
                            "Travelling from", state.current_city, "to", state.destination_city
                            )
                            print("You now have ", player.money, " money left.")
                            pass
                        else:
                            #cannot afford
                            print("Not Enough Money!")
                            continue
                    else:
                        #not a valid route
                        print("Pick a route that is connected to where you are now!")
                        count += 1
                        #TODO check if there is ANY valid route or if player ran out of money
                        continue
                    continue
                #then check if the player can afford it (if valid)
                # start = cities[state.current_city]
                # state.destination_city = action
                # destination = cities[state.destination_city]
                # player_sprite.set_location(cities[state.current_city])
                # state.travelling = True
                # print(
                #     "Travelling from", state.current_city, "to", state.destination_city
                # )

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        #displayCityNames(cities, city_names)
        for i, name in enumerate(city_names):
            text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
            screen.blit(text_surface, cities[i])

        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            result = run_pygame_combat(combat_surface, screen, player_sprite)
            if result == 1 or result == 0:
                #pay player
                player.money += 200
                print("You now have ", player.money)
                draw_journal_picture()
                pass
            elif result == -1:
                #you lose - end game
                print("You were defeated by the combatant! Game over.")
                break
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break

if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1

    screen = setup_window(width, height, "Game World Gen Practice")

    landscape_surface = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)
    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    cities = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:10]

    player_sprite = Sprite(sprite_path, cities[start_city])

    player = PyGameHumanPlayer()

    """ Add a line below that will reset the player variable to
    a new object of PyGameAIPlayer class."""
    player = PyGameAIPlayer()

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )

    while True:
        action = player.selectAction(state)
        #had to change some lines of code since AI is not returning an action to be casted, just an int
        #if 0 <= int(chr(action)) <= 9:
        if 0 <= action <= 9:
            #if int(chr(action)) != state.current_city and not state.travelling:
            if action != state.current_city and not state.travelling:
                start = cities[state.current_city]
                #state.destination_city = int(chr(action))
                state.destination_city = action
                destination = cities[state.destination_city]
                player_sprite.set_location(cities[state.current_city])
                state.travelling = True
                print(
                    "Travelling from", state.current_city, "to", state.destination_city
                )

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            run_pygame_combat(combat_surface, screen, player_sprite)
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break
