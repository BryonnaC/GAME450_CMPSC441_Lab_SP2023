import sys
import pygame
import random
from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab11.sprite import Sprite
from lab11.pygame_combat import run_pygame_combat
from lab11.pygame_human_player import PyGameHumanPlayer
from lab11.landscape import get_landscape, get_combat_bg
from lab11.pygame_ai_player import PyGameAIPlayer

from lab11.agent_environment import psuedo_agent_environ_main
from lab11.agent_environment import State

from lab2.cities_n_routes import get_randomly_spread_cities, get_routes

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)

if __name__ == "__main__":
    psuedo_agent_environ_main()