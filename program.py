import random

class Program:
    def _random_instruction(self, register_count, operations):
        op = random.choice(operations)
        z_index = random.randint(0, register_count - 1)
        x_index = random.randint(0, register_count - 1)
        y_index = random.randint(0, register_count - 1)
        return [op, z_index, x_index, y_index]
    def __init__(self, instruction_count, register_count, output_value_count, operations=None, register_initializer=None):
        if output_value_count > register_count:
            raise ValueError("Number of output values cannot exceed total number of registers.")
        if operations != None and register_initializer != None:
            self.instructions = [self._random_instruction(register_count, operations) for i in range(instruction_count)]
            self.initial_values = [register_initializer(i) for i in range(register_count)]
        self.instruction_count = instruction_count
        self.register_count = register_count
        self.output_value_count = output_value_count
    def copy(self):
        new_program = Program(self.instruction_count, self.register_count, self.output_value_count)
        # Copies the instructions.
        new_program.instructions = [[x for x in instruction] for instruction in self.instructions]
        # Copies the initial register values.
        new_program.initial_values = [x for x in self.initial_values]
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
        print("read_input_into_registers()")
        print("# Start of Program")
        # Print the program instructions.
        for i in range(self.instruction_count):
            op = self.instructions[i][0]
            z_index = self.instructions[i][1]
            x_index = self.instructions[i][2]
            y_index = self.instructions[i][3]
            print(op.expression.format(z_index, x_index, y_index))
        print("# End of Program")
    def without_introns(self):
        '''Returns a copy of this program with introns removed.'''
        raise NotImplementedError()
    def execute(self, *input_values, timeout=None):
        '''Executes the program and returns the output.'''
        if len(input_values) > self.register_count:
            raise ValueError("Number of input values cannot exceed total number of registers.")
        # Builds a list of registers.
        registers = [x for x in self.initial_values]
        # Sets the values of the input registers.
        for i in range(len(input_values)):
            registers[i] = input_values[i]
        if timeout == None:
            timeout = 100 * self.instruction_count
        # Initializes the program counter and time.
        program_counter = 0
        time = 0
        while program_counter < self.instruction_count and time < timeout:
            # Parses the instruction.
            (op, z_index, x_index, y_index) = self.instructions[program_counter]
            # Gets the values in the registers.
            x,y,z = registers[x_index], registers[y_index], registers[z_index]
            # Executes the instruction.
            registers[z_index], program_counter = op.behavior(x, y, z, program_counter)
            # Increments the time.
            time += 1
        # Returns the values in the output registers.
        return registers[:self.output_value_count]