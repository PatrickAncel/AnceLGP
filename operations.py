import math
import torch

class Operation:
    def __init__(self, behavior, expression, name):
        self.behavior = behavior
        self.expression = expression
        self.name = name
    def __repr__(self):
        return self.name

def b2f(bl):
    '''Converts a bool into a float.'''
    return 1.0 if bl else 0.0

epsilon = 1e-300
inf = float("inf")

def overflow_protected(f, x):
    try:
        return f(x)
    except OverflowError:
        return x

def domain_protected(f, x):
    try:
        return f(x)
    except ValueError:
        return x

def overflow_protected_sigmoid(x):
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        return 0.0

# Arithmetic
Addition =       Operation(lambda x, y, z, pc: (x + y, pc+1), "r{0} = r{1} + r{2}", "Addition")
Subtraction =    Operation(lambda x, y, z, pc: (x - y, pc+1), "r{0} = r{1} - r{2}", "Subtraction")
Multiplication = Operation(lambda x, y, z, pc: (x * y, pc+1), "r{0} = r{1} * r{2}", "Multiplication")
Division =       Operation(lambda x, y, z, pc: (x / y if y != 0 else y, pc+1), "r{0} = r{1} / r{2}", "Division")
Square =         Operation(lambda x, y, z, pc: (overflow_protected(lambda w: w**2, x), pc+1), "r{0} = r{1} ** 2", "Square")
SquareRoot =     Operation(lambda x, y, z, pc: (torch.sqrt(abs(x)) if type(x) == torch.Tensor else math.sqrt(abs(x)), pc+1), "r{0} = sqrt(|r{1}|)", "SquareRoot")
Exponent =       Operation(lambda x, y, z, pc: (overflow_protected(lambda w: (abs(w)+epsilon) ** y, x), pc+1), "r{0} = (|r{1}|+epsilon) ** r{2}", "Exponent")
Logarithm =      Operation(lambda x, y, z, pc: ((torch.log(abs(x)) if type(x) == torch.Tensor else math.log(abs(x))) if x != 0 else x, pc+1), "r{0} = ln(|r{1}|)", "Logarithm")

Sine =    Operation(lambda x, y, z, pc: (torch.sin(x) if type(x) == torch.Tensor else (math.sin(x) if math.isfinite(x) else 0.0), pc+1), "r{0} = sin(r{1})", "Sine")
Sigmoid = Operation(lambda x, y, z, pc: (torch.sigmoid(x) if type(x) == torch.Tensor else overflow_protected_sigmoid(x), pc+1), "r{0} = sigmoid(r{1})", "Sigmoid")

# Boolean
Conjunction =     Operation(lambda x, y, z, pc: (x and y, pc+1), "r{0} = r{1} and r{2}", "Conjunction")
Disjunction =     Operation(lambda x, y, z, pc: (x or y, pc+1), "r{0} = r{1} or r{2}", "Disjunction")
LogicalNegation = Operation(lambda x, y, z, pc: (b2f(not x), pc+1), "r{0} = not r{1}", "LogicalNegation")

# Control Flow
Conditional  = Operation(lambda x, y, z, pc: (z, pc+1 if z else pc+2), "if r{0}:", "Conditional")
IfThenGoBack = Operation(lambda x, y, z, pc: (z, max(0, pc-int(x)) if z else pc+1), "if r{0}, go back r{1} lines", "IfThenGoBack")