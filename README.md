# omnivariate-pso

Simple omnivariate particle swarm optimization.
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
import pso
import numpy as np
# Sinusoidal function
def sin(x):
    return np.sin(x)
# Auto optimization, with as few hyper-parameters as possible
best, coordinates = pso.optimize(sin, target='minimum', domain=[np.pi, 2*np.pi])
```

During this run, `best` is `-0.99999`, which is very close to `-1`.
`coordinates` is returned as the list: `[4.7123]` which is close to `3π/2`


### Optimizing a 5-dimensional function

Suppose we want to find the what combination values that comes closest to `4.3` of `f(x) = a^b+c/2-d/e` in the domain `-2.3 ≤ x ≤ 8` using `35` particles for `80` iterations with particle swarm optimization:

```python
from pso import optimize
# The function to optimize
def foo(a, b, c, d, e):
  return a**b + c/2 - d/e
# Initiate the PSO with 25 particles for 80 iterations
optimizer = PSO(n_particles=25, iters=80)
# Initiate the pso with 25 particles for 80 iterations
best, coordinates = optimizer.optimize(foo, target=4.3, domain=[-2.3, 8], n=35, iters=80)
```
