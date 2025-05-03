import sys
import math
import time

start_time = time.time()

from crossover import *
from fitness import *
from initializers import *
from mutation import *
from operations import *
from population import *
from program import *
from selection import *
import matplotlib.pyplot as plt

def plot_evolution(experiment_name, population, generation_count, stop_at_fitness):
    (generations, means, mins, all_time_best_fitness, all_time_best_program, all_custom_stats) = population.evolve(generation_count, stop_at_fitness)
    fig, ax = plt.subplots()
    ax.set_title(F"Best Fitness")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.plot(generations, mins)
    fig.savefig(F"results1/{experiment_name}-evolution.png")
    all_time_best_program.print_readable_code()
    print(mins)
    return (generations, means, mins, all_time_best_fitness, all_time_best_program, all_custom_stats)

def plot_1d_solution(experiment_name, x_test, y_test, program):
    y_hats = [program.execute(x)[0] for x in x_test]
    fig, ax = plt.subplots()
    ax.plot(x_test, y_test, label="Actual")
    ax.plot(x_test, y_hats, label="Predicted")
    ax.legend()
    fig.savefig(F"results1/{experiment_name}-1d-solution.png")

def plot_2d_solution(experiment_name, X, Y, Z):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0)
    fig.savefig(F"results1/{experiment_name}-1d-solution.png")

funcs = [lambda x: 0.3*x**2, lambda x,y: abs(x)**3.431 - 1.165*y, lambda x,y: math.sin(0.1*y)*x+25]
experiment_name = sys.argv[1]
function_number = int(sys.argv[2])
target_func = funcs[function_number]
operations = [Addition, Subtraction, Multiplication, Division, Square, SquareRoot, Exponent, Logarithm]
training_prob = float(sys.argv[3])
learning_rate = float(sys.argv[4])
generations = int(sys.argv[5])

# One-argument functions
if function_number == 0:
    x_train = np.linspace(-10, 10, 100).tolist()
    y_train = [target_func(x) for x in x_train]

    x_gd_train = np.linspace(-10, 10, 25).tolist()
    y_gd_train = [target_func(x) for x in x_gd_train]
# Two-argument functions
else:
    x_train = [(20 * random.random() - 10, 20 * random.random() - 10) for i in range(100)]
    y_train = [target_func(x1,x2) for (x1,x2) in x_train]
    x_gd_train = [(20 * random.random() - 10, 20 * random.random() - 10) for i in range(25)]
    y_gd_train = [target_func(x1,x2) for (x1,x2) in x_gd_train]

gd_fitness_func = mse_fitness_tensor(x_train, y_train)
custom_mutation_func = combined_mutation(
    standard_mutation(operations, 0.3, 0.1),
    gradient_descent_mutation(training_prob, learning_rate, 2, gd_fitness_func)
)
fitness_func = mse_fitness(x_train, y_train)
selection_func = binary_tournament_selection
program_mutation_rate = 1.0
crossover_rate = 0.5
instruction_count = 10
register_count = 4
input_value_count = 1 if function_number == 0 else 2
output_value_count = 1
register_initializer = RI_always_one
crossover_func=standard_crossover_2pt()
survival_selection_func = binary_tournament_selection
lam = 1000
nu = 500
mu = 1000

pop = Population(lam, nu, mu, selection_func, custom_mutation_func, program_mutation_rate, \
    crossover_rate, instruction_count, register_count, input_value_count, output_value_count, \
    operations, register_initializer, fitness_func, crossover_func, survival_selection_func, mu_plus_lambda=True)

(generations, means, mins, all_time_best_fitness, all_time_best_program, all_custom_stats) = plot_evolution(experiment_name, pop, generations, 0.0)
print(F"Time: {time.time() - start_time}")


with open(F"results1/{experiment_name}-result.txt", "w") as f:
    f.write(str(all_time_best_fitness))