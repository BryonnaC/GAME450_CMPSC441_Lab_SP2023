'''
Lab 12: Beginnings of Reinforcement Learning
We will modularize the code in pygrame_combat.py from lab 11 together.

Then it's your turn!
Create a function called run_episode that takes in two players
and runs a single episode of combat between them.
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.
Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.
Reward is the reward for the player for that turn.
'''
import sys
from pathlib import Path
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab11.turn_combat import Combat
from lab11.pygame_combat import run_turn, PyGameComputerCombatPlayer
from lab11.pygame_ai_player import PyGameAICombatPlayer
from lab11.pygame_human_player import PyGameHumanCombatPlayer


def run_episode(episode_of_combat, player1, player2):
    players = [player1, player2]

    #while not episode_of_combat.gameOver:
    reward = run_turn(episode_of_combat, player1, player2, players)

    action = [player1.weapon, player2.weapon]

    player1_health = player1.health
    player2_health = player2.health
    observation = [player1_health, player2_health]

    return [observation, action, reward]

    pass


if __name__ == "__main__":
    episode_of_combat = Combat()

    player = PyGameAICombatPlayer("Alexa")

    opponent = PyGameComputerCombatPlayer("Computer")

    while not episode_of_combat.gameOver:
        run_episode(episode_of_combat, player, opponent)

