import random

def RI_always_one(index):
    '''Assigns every register the value 1.'''
    return 1

def RI_identity(index):
    '''Assigns every register a value equal to its index.'''
    return index

def RI_uniform(index):
    '''Assigns every register a uniform random number between 0 and 1.'''
    return random.uniform(0, 1)

def RI_normal(index):
    '''Assigns every register a normally distributed random number with mean 0 and standard deviation 1.'''
    return random.gauss(0.0, 1.0)