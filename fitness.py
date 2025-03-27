import numpy as np

def mse_fitness_func_full(program, x_train, y_train, timeout):
    error = np.zeros_like([y_train[0]] if type(y_train[0]) in [int, float] else y_train[0])
    for i in range(len(x_train)):
        x = x_train[i]
        y = y_train[i]
        if type(x) in [int, float]:
            x = [x]
        if type(y) in [int, float]:
            y = [y]
        y = np.array(y)
        y_hat = np.array(program.execute(*x, timeout=timeout))
        error += (y - y_hat) ** 2
    error = error / len(x_train)
    fitness = error.sum().item()
    return fitness

def mse_fitness(x_train, y_train, timeout=None):
    return lambda program : mse_fitness_func_full(program, x_train, y_train, timeout)