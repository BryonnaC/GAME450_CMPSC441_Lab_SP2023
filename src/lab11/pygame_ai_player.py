import pygame
from lab11.turn_combat import CombatPlayer
""" Create PyGameAIPlayer class here"""


class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):
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

    
    pass
