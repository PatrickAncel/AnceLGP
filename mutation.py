import random

def mutate_instruction(instruction, register_count, operations, instruction_mutation_rate):
    '''Mutates an instruction with the specified probability.'''
    # Sets the new instruction to be the same as the old one with the operator or one of the registers or nothing changed.
    new_instruction = [part for part in instruction]
    if random.random() < instruction_mutation_rate:
        # Picks a random component of the instruction to change.
        part_to_change = random.randint(0,3)
        if part_to_change == 0:
            new_instruction[0] = random.choice(operations)
        else:
            new_instruction[part_to_change] = random.randint(0, register_count-1)
    return new_instruction

def mutation_func_full(program, register_count, operations, instruction_mutation_rate, register_mut_stdev):
    new_program = program.copy()
    new_program.initial_values = [random.gauss(value, register_mut_stdev) for value in program.initial_values]
    new_program.instructions = [mutate_instruction(instruction, register_count, operations, instruction_mutation_rate) for instruction in program.instructions]
    return new_program

def standard_mutation(operations, instruction_mutation_rate, register_mut_stdev):
    return lambda program, register_count : mutation_func_full(program, register_count, operations, instruction_mutation_rate, register_mut_stdev)