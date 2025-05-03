import random
import numpy as np
import math

class Program:
    def _random_instruction(self, register_count, input_value_count, operations):
        op = random.choice(operations)
        z_index = random.randint(0, register_count - 1)
        x_index = random.randint(-input_value_count, register_count - 1)
        y_index = random.randint(-input_value_count, register_count - 1)
        return [op, z_index, x_index, y_index]
    def __init__(self, instruction_count, register_count, input_value_count, output_value_count, operations=None, register_initializer=None):
        if output_value_count > register_count:
            raise ValueError("Number of output values cannot exceed total number of registers.")
        if operations != None and register_initializer != None:
            self.instructions = [self._random_instruction(register_count, input_value_count, operations) for i in range(instruction_count)]
            self.initial_values = [register_initializer(i) for i in range(register_count)]
        # self.instruction_count = instruction_count
        self.register_count = register_count
        self.input_value_count = input_value_count
        self.output_value_count = output_value_count
        self.parent_fitness = None
        self.semantic_vector = None
    def copy(self, parent_fitness = None):
        new_program = Program(len(self.instructions), self.register_count, self.input_value_count, self.output_value_count)
        # Copies the instructions.
        new_program.instructions = [[x for x in instruction] for instruction in self.instructions]
        # Copies the initial register values.
        new_program.initial_values = [x for x in self.initial_values]
        if parent_fitness == None:
            # Copies the parent fitness.
            new_program.parent_fitness = self.parent_fitness
        else:
            # Sets the specified parent fitness.
            new_program.parent_fitness = parent_fitness
        return new_program
    def unique_name(self):
        '''Returns a string that uniquely identifies this program.'''
        code = ";".join([F"{instruction[0].name},{instruction[1]},{instruction[2]},{instruction[3]}" for instruction in self.instructions])
        data = ",".join([str(value) for value in self.initial_values])
        return F"{code}#{data}"
    def print_readable_code(self):
        '''Prints out each instruction in the program code.'''
        print("# Register Initialization")
        # Print the register initializations.
        for i in range(self.register_count):
            print(F"r{i} = {self.initial_values[i]}")
        print("# Start of Program")
        # Print the program instructions.
        for i in range(len(self.instructions)):
            op = self.instructions[i][0]
            z_index = self.instructions[i][1]
            x_index = self.instructions[i][2]
            y_index = self.instructions[i][3]
            print(F"{i+1:>2}.  " + op.expression.format(z_index, x_index, y_index))
        print("# End of Program")
    def without_introns(self):
        '''Returns a copy of this program with introns removed.'''
        raise NotImplementedError()
    def execute(self, *input_values, timeout=None, calc_semantic_vector=False):
        '''Executes the program and returns the output.'''
        if len(input_values) != self.input_value_count:
            raise ValueError("Incorrect number of input values provided.")
        # if len(input_values) > self.register_count:
            # raise ValueError("Number of input values cannot exceed total number of registers.")
        # Builds a list of registers.
        registers = [x for x in self.initial_values]
        # # Sets the values of the input registers.
        # for i in range(len(input_values)):
        #     registers[i] = input_values[i]
        if timeout == None:
            timeout = 100 * len(self.instructions)
        # Initializes the program counter and time.
        program_counter = 0
        time = 0
        if calc_semantic_vector:
            semantic_vector = [np.array([r for r in registers])]
        while program_counter < len(self.instructions) and time < timeout:
            # Parses the instruction.
            (op, z_index, x_index, y_index) = self.instructions[program_counter]
            # Gets the values in the registers or input values.
            x = registers[x_index] if x_index >= 0 else input_values[-x_index-1]
            y = registers[y_index] if y_index >= 0 else input_values[-y_index-1]
            z = registers[z_index] if z_index >= 0 else input_values[-z_index-1]
            # x,y,z = registers[x_index], registers[y_index], registers[z_index]
            # Executes the instruction.
            registers[z_index], program_counter = op.behavior(x, y, z, program_counter)
            # Increments the time.
            time += 1
            if calc_semantic_vector:
                semantic_vector.append(np.array([r for r in registers]))
        if calc_semantic_vector:
            difference_vector = []
            for i in range(1, len(semantic_vector)):
                difference_vector.append(np.abs(semantic_vector[i] - semantic_vector[i-1]))
            sum_vector = np.array(difference_vector).sum(1)
            if self.semantic_vector == None:
                self.semantic_vector = [sum_vector]
            else:
                self.semantic_vector.append(sum_vector)
        # Returns the values in the output registers.
        return registers[:self.output_value_count]
    def semantic_intron_ratio(self):
        '''Returns the proportion of instructions that are semantic introns. Requires the semantic vector to be calculated.'''
        if self.semantic_vector == None:
            raise Exception("Semantic vector not calculated.")
        intron_count = 0
        # Iterates over every instruction index.
        for i in range(len(self.instructions)):
            significance_found = False
            # Iterates over every fitness case.
            for sum_vector in self.semantic_vector:
                if math.isnan(sum_vector[i]) or sum_vector[i] > 1e-10:
                    significance_found = True
                    break
            if not significance_found:
                intron_count += 1
        return intron_count / len(self.instructions)
    def get_structural_introns(self):
        '''Returns the indices of instructions that are structural introns. Only works for code without branching instructions.'''
        effective_registers = [i for i in range(self.output_value_count)]
        marked_instructions = []
        for i in range(len(self.instructions)-1, -1, -1):
            instruction = self.instructions[i]
            if instruction[1] in effective_registers:
                marked_instructions.append(i)
                effective_registers.append(instruction[2])
                effective_registers.append(instruction[3])
        return [i for i in range(len(self.instructions)) if i not in marked_instructions]
    def structural_intron_ratio(self):
        '''Returns the proportion of instructions that are structural introns.'''
        return len(self.get_structural_introns()) / len(self.instructions)