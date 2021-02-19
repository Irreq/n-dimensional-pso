# n-dimensional-pso

Simple N-dimensional particle swarm optimization.
This is a semi-automatic tool to find
points-of-interest (PoI) within a function.

* **No Libraries:** Clone this project `git clone https://github.com/irreq/n-dimensional-pso` and start optimizing!
* **Dimensional Independent:** Higher dimensions do however require more computational power.
* **Simplicity:** Just feed the name of the function to optimize, and out comes a solution.

## Definition

In computational science, particle swarm optimization (PSO) is a computational method that optimizes a problem by iteratively trying to improve a candidate solution with regard to a given measure of quality. It solves a problem by having a population of candidate solutions, here dubbed particles, and moving these particles around in the search-space according to simple mathematical formulae over the particle's position and velocity. Each particle's movement is influenced by its local best known position, but is also guided toward the best known positions in the search-space, which are updated as better positions are found by other particles. This is expected to move the swarm toward the best solutions. (https://en.wikipedia.org/wiki/Particle_swarm_optimization)

## Usage

### Optimizing a sinusoidal function

Suppose we want to find the minima of `f(x) = sin(x)` in the domain: `π ≤ x ≤ 2π`.
The known solution is `x = 3π/2` where `sin(3π/2) = -1`
Using particle swarm optimization:

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
minimum, coordinates = optimizer.optimize(sin, 'minimum', domain=[np.pi, 2*np.pi])
```

### Optimizing a 5-dimensional function

Suppose we want to find the maxima of `f(x) = a^b+c/2-d/e` using particle swarm optimization:

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
maximum, coordinates = optimizer.optimize(sin, 'maximum', domain=[-2, 8])
```
