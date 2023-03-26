import pygame
from lab11.turn_combat import CombatPlayer
import random
""" Create PyGameAIPlayer class here"""


class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):
        #need to select a number if in map
        #okay lets choose a random number
        #the code in agent environment will make sure its not current city
        city_choice = random.randint(0,10)
        return city_choice
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if ord("0") <= event.key <= ord("9"):
                    return event.key
        return ord(str(state.current_city))  # Not a safe operation for >10 cities

    pass


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        while True:
            choice = random.randint(0,2)
            self.weapon = choice
            return self.weapon

    pass
