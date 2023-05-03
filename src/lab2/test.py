'''
size = (100, 200)   #like an array - is a tuple

cities = [ ]

for i in range(10):
    cities.append()

#return cities
'''
import itertools    #built in API, generate all possible combinations of 2 things

a = ['a', 'b', 'c']

for acombo in itertools.combinations(a, 2):
    print(acombo)

import random
random.randint()