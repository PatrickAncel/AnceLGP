import random

def crossover_1pt_func_full(program1, program2):
    '''Length-preserving 1pt crossover. Works for programs of the same length.'''
    program_length = len(program1.instructions)
    crossover_point = random.randint(1, program_length-1)
    # Copies the instructions.
    new_program1 = program1.copy()
    new_program2 = program2.copy()
    new_program1.instructions = [program1.instructions[i] if i < crossover_point else program2.instructions[i] for i in range(program_length)]
    new_program2.instructions = [program2.instructions[i] if i < crossover_point else program1.instructions[i] for i in range(program_length)]
    return (new_program1, new_program2)

def standard_crossover_1pt():
    '''Performs length-preserving one-point crossover on two programs of the same length.'''
    return lambda program1, program2 : crossover_1pt_func_full(program1, program2)

def crossover_2pt_func_full(program1, program2):
    '''Length-preserving 2pt crossover. Works for programs of the same length.'''
    program_length = len(program1.instructions)
    crossover_points = [random.randint(1, program_length-1) for i in range(2)]
    crossover_point_1 = min(crossover_points)
    crossover_point_2 = max(crossover_points)
    # Copies the instructions.
    new_program1 = program1.copy()
    new_program2 = program2.copy()
    new_program1.instructions = [program1.instructions[i] if i not in range(crossover_point_1, crossover_point_2) else program2.instructions[i] for i in range(program_length)]
    new_program2.instructions = [program2.instructions[i] if i not in range(crossover_point_1, crossover_point_2) else program1.instructions[i] for i in range(program_length)]
    return (new_program1, new_program2)

def standard_crossover_2pt():
    '''Performs length-preserving two-point crossover on two programs of the same length.'''
    return lambda program1, program2 : crossover_2pt_func_full(program1, program2)

def var_length_crossover_func_full(program1, program2):
    program_length1 = len(program1.instructions)
    program_length2 = len(program2.instructions)
    crossover_point1 = random.randint(0, program_length1)
    crossover_point2 = random.randint(0, program_length2)
    new_program1 = program1.copy()
    new_program2 = program2.copy()
    new_program1.instructions = program1.instructions[:crossover_point1] + program2.instructions[crossover_point2:]
    new_program2.instructions = program2.instructions[:crossover_point2] + program1.instructions[crossover_point1:]
    return (new_program1, new_program2)

def var_length_crossover():
    return lambda program1, program2 : var_length_crossover_func_full(program1, program2)