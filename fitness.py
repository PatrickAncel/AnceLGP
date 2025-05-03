import math
import numpy as np
import torch

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
    if math.isnan(fitness):
        fitness = math.inf
    return fitness

def mse_fitness(x_train, y_train, timeout=None):
    return lambda program : mse_fitness_func_full(program, x_train, y_train, timeout)

def mse_fitness_with_softmax_func_full(program, x_train, y_train, timeout):
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
        # Softmax here
        y_hat = np.exp(y_hat - y_hat.max())
        y_hat = y_hat / y_hat.sum()
        error += (y - y_hat) ** 2
    error = error / len(x_train)
    fitness = error.sum().item()
    if math.isnan(fitness):
        fitness = math.inf
    return fitness

def mse_fitness_with_softmax(x_train, y_train, timeout=None):
    return lambda program : mse_fitness_with_softmax_func_full(program, x_train, y_train, timeout)

def mse_tensor_fitness_with_softmax_func_full(program, x_train, y_train, timeout):
    error = torch.tensor(0.0, requires_grad=True)
    for i in range(len(x_train)):
        x = x_train[i]
        y = y_train[i]
        if type(x) in [int, float]:
            x = [x]
        if type(y) in [int, float]:
            y = [y]
        y_hat = program.execute(*x, timeout=timeout)
        # Finds the maximum of y_hat.
        y_hat_max = y_hat[0]
        for j in range(i, len(y_hat)):
            if y_hat[j] > y_hat_max:
                y_hat_max = y_hat[j]
        # Subtracts the largest element from y_hat and exponentiates each.
        # Also keeps a sum of all exponentiated terms.
        y_hat_total = torch.tensor(0.0)
        for j in range(len(y_hat)):
            y_hat[j] = torch.exp(y_hat[j] - y_hat_max) if type(y_hat[j]) == torch.Tensor else math.exp(y_hat[j] - y_hat_max)
            y_hat_total = y_hat_total + y_hat[j]
        # Divides each term by the total.
        for j in range(len(y_hat)):
            y_hat[j] = y_hat[j] / y_hat_total
        for j in range(len(y_hat)):
            error = error + (y[j] - y_hat[j]) ** 2
    error = error / len(x_train)
    fitness = error
    return fitness

def mse_tensor_fitness_with_softmax(x_train, y_train, timeout=None):
    return lambda program : mse_tensor_fitness_with_softmax_func_full(program, x_train, y_train, timeout)

def mse_fitness_semantic_vector_func_full(program, x_train, y_train, timeout):
    error = np.zeros_like([y_train[0]] if type(y_train[0]) in [int, float] else y_train[0])
    for i in range(len(x_train)):
        x = x_train[i]
        y = y_train[i]
        if type(x) in [int, float]:
            x = [x]
        if type(y) in [int, float]:
            y = [y]
        y = np.array(y)
        y_hat = np.array(program.execute(*x, timeout=timeout, calc_semantic_vector=True))
        error += (y - y_hat) ** 2
    error = error / len(x_train)
    fitness = error.sum().item()
    return fitness

def mse_fitness_semantic_vector(x_train, y_train, timeout=None):
    return lambda program : mse_fitness_semantic_vector_func_full(program, x_train, y_train, timeout)


def mse_tensor_fitness_func_full(program, x_train, y_train, timeout):
    error = torch.tensor(0.0, requires_grad=True)
    for i in range(len(x_train)):
        x = x_train[i]
        y = y_train[i]
        if type(x) in [int, float]:
            x = [x]
        if type(y) in [int, float]:
            y = [y]
        y_hat = program.execute(*x, timeout=timeout)
        for j in range(len(y_hat)):
            error = error + (y[j] - y_hat[j]) ** 2
    error = error / len(x_train)
    fitness = error
    return fitness

def mse_fitness_tensor(x_train, y_train, timeout=None):
    return lambda program : mse_tensor_fitness_func_full(program, x_train, y_train, timeout)

def classifier_accuracy_func_full(program, x_test, y_test, timeout):
    correct_count = 0
    for i in range(len(x_test)):
        x = x_test[i]
        y = y_test[i]
        if type(x) in [int, float]:
            x = [x]
        y_hat = program.execute(*x, timeout=timeout)
        if np.argmax(y) == np.argmax(y_hat):
            correct_count += 1
    return -correct_count / len(x_test)

def classifier_accuracy(x_test, y_test, timeout=None):
    return lambda program : classifier_accuracy_func_full(program, x_test, y_test, timeout)