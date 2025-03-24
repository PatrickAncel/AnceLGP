import random
from itertools import accumulate

def roulette_wheel_selection(programs, fitness_func):
    # Gets the fitness of every program.
    fitnesses = [fitness_func(program) for program in programs]
    total_fitness = sum(fitnesses)
    # Normalizes the fitnesses.
    norm_fitness = [fitness / total_fitness for fitness in fitnesses]
    # Makes the fitness values cumulative.
    cumul_fitness = list(accumulate(norm_fitness))
    # Spins the roulette wheel.
    decision_marker = random.random()
    decision_index = None
    # Sees where the marker landed.
    for i in range(len(programs)):
        if decision_marker < cumul_fitness[i]:
            decision_index = i
            break
    if decision_index == None:
        decision_index = len(programs)-1
    # Returns a list containing the selected program.
    return [programs[decision_index]]

def binary_tournament_selection(programs, fitness_func):
    if len(programs) % 2 != 0:
        raise ValueError("binary_tournament_selection can only be used if lambda is divisible by two.")
    random.shuffle(programs)
    return [programs[i] if fitness_func(programs[i]) < fitness_func(programs[i + len(programs)//2]) else programs[i + len(programs)//2] for i in range(len(programs)//2)]