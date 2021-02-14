# n-dimensional-pso

Simple N-dimensional particle swarm optimization.
this is a semi-automatic tool to find
points-of-interest (PoI) within a function.

* **No Libraries** Clone this project `git clone https://github.com/irreq/n-dimensional-pso` and start optimizing!
* **Dimensional Independent:** Higher dimensions do however require more computational power.
* **Simplicity** Just feed the name of the function to optimize, and out comes a solution.

## Usage

### Optimizing a sinusoidal function

Suppose we want to find the maxima of `f(x) = sin(x)` using particle swarm optimization:

```python
from pso import PSO
import numpy as np
# Sinusoidal function
def sin(x):
    return np.sin(x)
# Number of particles to use
n = 25
# Initiate the PSO
optimizer = PSO(agents=n)
# Auto optimization, with as few hyperparameters as possible
maximum, coordinates = optimizer.optimize(sin, 'maximum', domain=[np.pi, 2*np.pi])
```

### Optimizing a 5-dimensional function

Suppose we want to find the minima of `f(x) = a^b+c/2-d/e` using particle swarm optimization:

```python
from pso import PSO
import numpy as np
# The function to optimize
def foo(a, b, c, d, e):
  return a**b + c/2 - d/e
# Number of particles to use
n = 15
# Initiate the PSO
optimizer = PSO(agents=n, iters=80)
# Auto optimization, with as few hyperparameters as possible
maximum, coordinates = optimizer.optimize(sin, 'minimum', domain=[-2, 8])
```
