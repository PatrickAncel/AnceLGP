import math

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

def overflow_protected(f):
    try:
        return f()
    except OverflowError:
        return inf

# Arithmetic
Addition =       Operation(lambda x, y, z, pc: (x + y, pc+1), "r{0} = r{1} + r{2}", "Addition")
Subtraction =    Operation(lambda x, y, z, pc: (x - y, pc+1), "r{0} = r{1} - r{2}", "Subtraction")
Multiplication = Operation(lambda x, y, z, pc: (x * y, pc+1), "r{0} = r{1} * r{2}", "Multiplication")
Division =       Operation(lambda x, y, z, pc: (x / y if y != 0 else 0, pc+1), "r{0} = r{1} / r{2}", "Division")
Square =         Operation(lambda x, y, z, pc: (overflow_protected(lambda : x**2), pc+1), "r{0} = r{1} ** 2", "Square")
SquareRoot =     Operation(lambda x, y, z, pc: (math.sqrt(abs(x)), pc+1), "r{0} = sqrt(|r{1}|)", "SquareRoot")
Exponent =       Operation(lambda x, y, z, pc: (overflow_protected(lambda : (abs(x)+epsilon) ** y), pc+1), "r{0} = (|r{1}|+epsilon) ** r{2}", "Exponent")
Logarithm =      Operation(lambda x, y, z, pc: (math.log(abs(x)) if x != 0 else 0, pc), "r{0} = ln(|r{1}|)", "Logarithm")

# Boolean
Conjunction =     Operation(lambda x, y, z, pc: (x and y, pc+1), "r{0} = r{1} and r{2}", "Conjunction")
Disjunction =     Operation(lambda x, y, z, pc: (x or y, pc+1), "r{0} = r{1} or r{2}", "Disjunction")
LogicalNegation = Operation(lambda x, y, z, pc: (b2f(not x), pc+1), "r{0} = not r{1}", "LogicalNegation")

# Control Flow
Conditional  = Operation(lambda x, y, z, pc: (z, pc+1 if z else pc+2), "if r{0}:", "Conditional")
IfThenGoBack = Operation(lambda x, y, z, pc: (z, max(0, pc-int(x)) if z else pc+1), "if r{0}, go back r{1} lines", "IfThenGoBack")