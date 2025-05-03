import random
import torch
import math

def mutate_instruction(instruction, register_count, input_value_count, operations, instruction_mutation_rate):
    '''Mutates an instruction with the specified probability.'''
    # Sets the new instruction to be the same as the old one with the operator or one of the registers or nothing changed.
    new_instruction = [part for part in instruction]
    if random.random() < instruction_mutation_rate:
        # Picks a random component of the instruction to change.
        part_to_change = random.randint(0,3)
        if part_to_change == 0:
            new_instruction[0] = random.choice(operations)
        elif part_to_change == 1:
            new_instruction[part_to_change] = random.randint(0, register_count-1)
        else:
            new_instruction[part_to_change] = random.randint(-input_value_count, register_count-1)
    return new_instruction

def mutation_func_full(program, register_count, input_value_count, operations, instruction_mutation_rate, register_mut_stdev):
    new_program = program.copy()
    new_program.initial_values = [random.gauss(value, register_mut_stdev) for value in program.initial_values]
    new_program.instructions = [mutate_instruction(instruction, register_count, input_value_count, operations, instruction_mutation_rate) for instruction in program.instructions]
    return new_program

def standard_mutation(operations, instruction_mutation_rate, register_mut_stdev):
    return lambda program, register_count, input_value_count : mutation_func_full(program, register_count, input_value_count, operations, instruction_mutation_rate, register_mut_stdev)

def random_generation_mutation_func(program, register_count, input_value_count, operations, register_initializer):
    '''Returns a completely new program with the same number of instructions as the parent.'''
    new_program = program.copy()
    new_program.initial_values = [register_initializer(i) for i in range(register_count)]
    new_program.instructions = [program._random_instruction(register_count, operations, input_value_count) for i in range(len(program.instructions))]
    return new_program

def random_generation_mutation(operations, register_initializer):
    return lambda program, register_count, input_value_count : random_generation_mutation_func(program, register_count, input_value_count, operations, register_initializer)

def perform_gradient_descent(program, register_count, input_value_count, train_prob, learning_rate, num_epochs, fitness_func):
    if random.random() < train_prob:
        new_program = program.copy()
        # initial_register_values = [torch.tensor(r, requires_grad=True) for r in new_program.initial_values]
        # new_program.initial_values = [r for r in initial_register_values]
        new_program.initial_values = [torch.tensor(r, requires_grad=True) for r in new_program.initial_values]
        # print(F"\nGD Training: Epoch 0 of {num_epochs}\t\t\t\t\t", end="")
        try:
            for epoch in range(num_epochs):
                # print(F"\rGD Training: Epoch {epoch+1} of {num_epochs}\t\t\t\t\t", end="")
                # Resets the gradients of the initial values.
                for r in new_program.initial_values:
                    r.grad = None
                # Calculates the fitness.
                fitness = fitness_func(new_program)
                # Backpropagates the gradients.
                fitness.backward()
                # Updates the initial register values.
                for i in range(len(new_program.initial_values)):
                    # print(r.grad)
                    r = new_program.initial_values[i]
                    new_program.initial_values[i] = r - learning_rate * (r.grad if r.grad != None and not math.isnan(r.grad.item()) else 0.0)
            # print("\rGD Training Done.\t\t\t\t\t\t\t\t\t\t\t\t\t")
        # If an overflow error occurs while computing fitness, gradient descent will probably not help this program.
        except OverflowError:
            pass
        new_program.initial_values = [r.item() for r in new_program.initial_values]
        # print(new_program.initial_values)
        # print(new_program.initial_values)
        return new_program
    else:
        return program

def gradient_descent_mutation(train_prob, learning_rate, num_epochs, fitness_func):
    return lambda program, register_count, input_value_count : perform_gradient_descent(program, register_count, input_value_count, train_prob, learning_rate, num_epochs, fitness_func)

def combined_mutation_func_full(program, register_count, input_value_count, mutation_funcs):
    for mutation_func in mutation_funcs:
        program = mutation_func(program, register_count, input_value_count)
    return program

def combined_mutation(*mutation_funcs):
    return lambda program, register_count, input_value_count : combined_mutation_func_full(program, register_count, input_value_count, mutation_funcs)