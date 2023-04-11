'''
Lab 13: My first AI agent.
In this lab, you will create your first AI agent.
You will use the run_episode function from lab 12 to run a number of episodes
and collect the returns for each state-action pair.
Then you will use the returns to calculate the action values for each state-action pair.
Finally, you will use the action values to calculate the optimal policy.
You will then test the optimal policy to see how well it performs.

Sidebar-
If you reward every action you may end up in a situation where the agent
will always choose the action that gives the highest reward. Ironically,
this may lead to the agent losing the game.
'''
import sys
from pathlib import Path

# line taken from turn_combat.py
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab11.pygame_combat import PyGameComputerCombatPlayer
from lab11.turn_combat import CombatPlayer
from lab12.episode import run_episode
from lab11.turn_combat import Combat
from lab11.pygame_ai_player import PyGameAICombatPlayer

from collections import defaultdict
import random
import numpy as np


class PyGameRandomCombatPlayer(PyGameComputerCombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        self.weapon = random.randint(0, 2)
        return self.weapon


class PyGamePolicyCombatPlayer(CombatPlayer):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy

    def weapon_selecting_strategy(self):
        self.weapon = self.policy[self.current_env_state]
        return self.weapon


def run_random_episode(player, opponent):
    curr_episode = Combat()

    player.health = random.choice(range(10, 110, 10))
    opponent.health = random.choice(range(10, 110, 10))

    return_list = [ ]
    while not curr_episode.gameOver:
        return_list.append(run_episode(curr_episode, player, opponent))

    return return_list


def get_history_returns(history):
    total_return = sum([reward for _, _, reward in history])
    returns = {}
    for i, (state, action, reward) in enumerate(history):
        if state not in returns:
            returns[state] = {}
        returns[state][action] = total_return - sum(
            [reward for _, _, reward in history[:i]]
        )
    return returns


def run_episodes(n_episodes):
    ''' Run 'n_episodes' random episodes and return the action values for each state-action pair.
        Action values are calculated as the average return for each state-action pair over the 'n_episodes' episodes.
        Use the get_history_returns function to get the returns for each state-action pair in each episode.
        Collect the returns for each state-action pair in a dictionary of dictionaries where the keys are states and
            the values are dictionaries of actions and their returns.
        After all episodes have been run, calculate the average return for each state-action pair.
        Return the action values as a dictionary of dictionaries where the keys are states and
            the values are dictionaries of actions and their values.
    '''
    history = [ ]
    dict_of_dict = { }
    action_values = { }
    returns = { }

    for i in range(0, n_episodes):
        #curr_episode = Combat()
        player = PyGameRandomCombatPlayer("Rando")
        opponent = PyGameComputerCombatPlayer("Computer")

        history = run_random_episode(player, opponent)

        returns = get_history_returns(history)

        #okay this is the most recent addition, this one follows logic of
        #check the state in returns, see if it alreay exists in dict of dict
        #if it does not - just make it
        #else find the nested dictionary and append the reward to the exist reward, making it a list
        #changes i expect to make are chaning "key" and also might need to look more specifically into state-action
        #in the if statement to decide if i already have the state-action pair or not instead of just the state
        for state in returns.keys():
            if state not in dict_of_dict.keys():
                dict_of_dict[state] = returns[state]
            else:
                for key, value_dict in dict_of_dict.items():
                    for key2, value in value_dict.items():
                        value.append(returns[key2])
                        pass
                    pass
            pass

        for _ in returns.keys():
            dict_of_dict[_] = returns[_]
            #dict_of_dict[state].update(returns[state]) #this doesn't work?? the key value pair has to be unique?
            #okay eavesdropping says to make rewards a list instead of just copying what returns has
        #dict_of_dict[state] = returns  #how get state? look into returns?? prob
        #collect returns from get history in a dictionary of dictionaries

    for state, returns in dict_of_dict.items():
        #num_rewards = 0
        for action, reward in returns.items():
            print(reward)
            #num_rewards += 1
        pass

    #now get average return for each state-action pair
    #for state in dict_of_dict.keys():
        #average_sum = 0
        #count = 0
        #this for loop is wrong. it's missing something
        #for action in dict_of_dict[state].keys():
            #state_act_sum = sum(dict_of_dict[state][action])
            #dict_of_dict[state][action].length()
            #count += 1
            #pass
        #average_state_act_pair = state_act_sum/count
        #sum(reward for [_][_]:reward in )
        #sum(reward for dict_of_dict[_][_]:reward)
        #sum_returns += dict_of_dict[_][_]
        #pass

    return action_values


def get_optimal_policy(action_values):
    optimal_policy = defaultdict(int)
    for state in action_values:
        optimal_policy[state] = max(action_values[state], key=action_values[state].get)
    return optimal_policy


def test_policy(policy):
    names = ["Legolas", "Saruman"]
    total_reward = 0
    for _ in range(100):
        player1 = PyGamePolicyCombatPlayer(names[0], policy)
        player2 = PyGameComputerCombatPlayer(names[1])
        players = [player1, player2]
        total_reward += sum(
            [reward for _, _, reward in run_episode(*players)]
        )
    return total_reward / 100


if __name__ == "__main__":
    #action_values = run_episodes(10000)
    action_values = run_episodes(2000)
    print(action_values)
    optimal_policy = get_optimal_policy(action_values)
    print(optimal_policy)
    print(test_policy(optimal_policy))
