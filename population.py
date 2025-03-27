import random
from program import Program

class Population:
    def __init__(self, lam, nu, mu, selection_func, mutation_func, program_mutation_rate, crossover_rate, instruction_count, register_count, output_value_count, operations, register_initializer, fitness_func, crossover_func=None, survival_selection_func=None, stats_gatherer=None, mu_plus_lambda=True):
        if nu > lam:
            raise ValueError("Negative selection pressure: nu cannot exceed lambda.")
        if mu < lam:
            raise ValueError("Insufficient reproduction level: mu cannot be less than lambda.")
        if mu % 2 != 0 and crossover_func != None:
            raise ValueError("Population size after reproduction (mu) must be divisible by 2 when crossover_func is not None.")
        if (mu_plus_lambda or mu > lam) and survival_selection_func == None:
            raise ValueError("Based on the chosen parameters, survival selection is required to keep the population size constant.")
        self.lam = lam
        self.nu = nu
        self.mu = mu
        self.selection_func = selection_func
        self.mutation_func = mutation_func
        self.crossover_func = crossover_func
        self.survival_selection_func = survival_selection_func
        self.fitness_func = fitness_func
        self.mu_plus_lambda = mu_plus_lambda
        self.program_mutation_rate = program_mutation_rate
        self.crossover_rate = crossover_rate
        self.register_count = register_count
        self.output_value_count = output_value_count
        if stats_gatherer == None:
            stats_gatherer = lambda population : []
        self.stats_gatherer = stats_gatherer
        # Initializes the population.
        self.members = [Program(instruction_count, register_count, output_value_count, operations, register_initializer) for i in range(lam)]
        self.next_members = []
        self._fitnesses = {}
    def _internal_fitness(self, program):
        '''Calculates the fitness of a program and stores it in the hash table, or reads its fitness from the table.'''
        key = program.unique_name()
        # If the fitness of the program is in the hash table...
        if key in self._fitnesses:
            # ... return the stored fitness.
            return self._fitnesses[key]
        # Else calculate the fitness of the program.
        fitness = self.fitness_func(program)
        # Store the fitness for later use.
        self._fitnesses[key] = fitness
        # Return the fitness.
        return fitness
    def select(self):
        '''Iteratively applies the selection function until the desired population size is achieved.'''
        # Initialize an empty "next" population.
        self.next_members = []
        # Until the "next" population size reaches nu...
        while len(self.next_members) < self.nu:
            # Select parents into the "child" population.
            self.next_members += self.selection_func(self.members, self._internal_fitness)
        # If too many parents have been selected...
        if len(self.next_members) > self.nu:
            # ...trims the parents.
            self.next_members = self.next_members[:self.nu]
    def reproduce(self):
        '''Copies population members verbatim until the desired population size is achieved.'''
        random.shuffle(self.next_members)
        # Until the "next" population reaches mu...
        while len(self.next_members) < self.mu:
            # Copy the existing "next" population members.
            self.next_members += [member.copy() for member in self.next_members]
        # If too many children have been created...
        if len(self.next_members) > self.mu:
            # ...trims the children.
            self.next_members = self.next_members[:self.mu]
    def mutate(self):
        '''Performs mutation over the entire population at the desired mutation rate.'''
        self.next_members = [self.mutation_func(program, self.register_count) if random.random() < self.program_mutation_rate else program.copy() for program in self.next_members]
    def crossover(self):
        '''Performs crossover over the entire population at the desired xover rate.'''
        random.shuffle(self.next_members)
        # Crosses over pairs of members.
        pairs = [self.crossover_func(self.next_members[2*i],self.next_members[2*i+1]) \
                if random.random() < self.crossover_rate \
                else (self.next_members[2*i].copy(), self.next_members[2*i+1].copy()) \
                for i in range(self.mu//2)]
        # Unpacks the pairs.
        self.next_members = [program for pair in pairs for program in pair]
    def reinsert_parents(self):
        '''If (mu+lambda) selection is enabled, appends self.next_members to self.members.
        Otherwise, replaces self.members with self.next_members.
        At the end, clears self.next_members.'''
        if self.mu_plus_lambda:
            self.members += self.next_members
        else:
            self.members = self.next_members
        self.next_members = []
    def select_survivors(self):
        '''Iterative applies the survivor selection function until the desired population size is achieved.'''
        if self.survival_selection_func != None:
            survivors = []
            # Until the survivor count reaches lambda...
            while len(survivors) < self.lam:
                random.shuffle(self.members)
                # Select survivors.
                survivors += self.survival_selection_func(self.members, self._internal_fitness)
            # If too many survivors have been selected...
            if len(survivors) > self.lam:
                # ...trims the survivors.
                survivors = survivors[:self.lam]
            self.members = survivors
    def _iterate(self):
        '''Performs one iteration of evolution.'''
        self.select()
        self.reproduce()
        self.mutate()
        self.crossover()
        self.reinsert_parents()
        self.select_survivors()
        # Captures statistics of the population.
        fitnesses = [self._internal_fitness(prog) for prog in self.members]
        mean_fitness = sum(fitnesses) / self.lam
        best_program_index = min(range(self.lam), key = lambda i : fitnesses[i])
        best_program = self.members[best_program_index]
        best_fitness = fitnesses[best_program_index]
        custom_stats = self.stats_gatherer(self)
        return (mean_fitness, best_fitness, best_program, custom_stats)
    def evolve(self, generation_count, stop_at_fitness=0.0):
        '''Performs evolution until reaching the maximum number of generations of achieving the fitness threshold.'''
        generations = []
        means = []
        mins = []
        all_time_best_fitness = float("inf")
        all_time_best_program = None
        all_custom_stats = []
        print("Beginning evolution.")
        for i in range(generation_count):
            print(F"\rCompleted {i}/{generation_count} generations. Best Fitness: {all_time_best_fitness}\t\t\t\t\t", end="")
            (mean_fitness, best_fitness, best_program, custom_stats) = self._iterate()
            generations.append(i)
            means.append(mean_fitness)
            mins.append(best_fitness)
            all_custom_stats.append(custom_stats)
            if best_fitness < all_time_best_fitness:
                all_time_best_fitness = best_fitness
                all_time_best_program = best_program
                if best_fitness <= stop_at_fitness:
                    print(F"\rStopping early. Completed {i+1}/{generation_count} generations. Best Fitness: {all_time_best_fitness}\t\t\t\t\t", end="")
                    break
            print(F"\rCompleted {i+1}/{generation_count} generations. Best Fitness: {all_time_best_fitness}\t\t\t\t\t", end="")
        print("\nEvolution complete.")
        return (generations, means, mins, all_time_best_fitness, all_time_best_program, all_custom_stats)
