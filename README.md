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

### Finding the square root of 2

Suppose we want to find `√2`. This could be done by finding what value `x` is when the function `power_2` (also known as `x^2`) returns `2` for `x`. Since we know the real answer is `1<x<2` we can specify the search domain for increased performance. Using particle swarm optimization:

```python
import pso
# The function to optimize
def power_2(x):
  return x**2
# Auto optimization, with as few hyper-parameters as possible
best, coordinates = pso.optimize(power_2, target=2, domain=[1, 2])
# [1.414211357351861] 1.9999937632629934
```

### Optimizing a sinusoidal function

Suppose we want to find the minima of `f(x) = sin(x)` in the domain: `π ≤ x ≤ 2π`.
The current known solution is `x = 3π/2` where `sin(3π/2) = -1`.
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


### Optimizing a multivariate 5-dimensional function

Suppose we want to find the what combination values that comes closest to `4.3` of `f(a,b,c,d,e) = a^b+c/2-d/e` in the chosen domain `-2.3 ≤ a,b,c,d,e ≤ 8` using `35` particles for `80` iterations.
Using particle swarm optimization:

```python
import pso
# The function to optimize
def foo(a, b, c, d, e):
  return a**b + c/2 - d/e
# Initiate the pso with 35 particles for 80 iterations
best, coordinates = pso.optimize(foo, target=4.3, domain=[-2.3, 8], n=35, iters=80)
```
