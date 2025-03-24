A *register initializer* is a function that sets the initial value of a register. It must accept a register index (int) as its parameter and return an int or float.

---

An operation is defined by three things: *behavior* an *expression*, and a name. The behavior is a function with four inputs: the inputs from registers, $x$ and $y$, the current value $z$ in the output register, and the program counter $c$. It returns a tuple whose first element is the value to write in the output register and whose second value is the new value of the program counter. For most operations, the value $z$ will be unused, and the new value of the program counter is $c+1$. Both of these features are intended for control flow operations.

The expression determines how a program instruction containing the operation is printed.

**Do not give different operations the same name within the same evolutionary run.** The name is used when hashing an instruction. Only use letters in the name.

---

The general outline of the algorithm loop is:
1. Selection
2. Reproduction
3. Mutation
4. Crossover
5. Reinsertion of Parents (optional)
6. Survival Selection (optional)

The initial population size is called $\lambda$. The population size after selection is called $\nu$. The population size after reproduction is called $\mu$. Mutation and crossover do not affect the population size. If $(\mu+\lambda)$ is used, or $\mu>\lambda$, then survival selection is required.