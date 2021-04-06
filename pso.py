#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pso.py
#
# Author : Irreq

"""
Omni Dimensional Particle Swarm Optimization
without external libraries (RAW Python)

DOCUMENTATION:          Read this or see: 'README.md' or read comments in
                        functions. Note functions: 'random' and 'uniform'
                        can be replaced by functions from the random module
                        with the same name. Eg, uniform() = random.uniform()

TODO:                   Finnish documentation
                        + the dancers and killers.
                        - dead code.
"""


e = 2.718281828459045235360287471352662497757


def random(multiplier=69069, increment=1, modulus=2**16):
    """
    Linear Congruential Generator (LCG)

    NOTE:                   A linear congruential generator (LCG) is
                            an algorithm that yields a sequence of
                            pseudo-randomized numbers calculated with a
                            discontinuous piecewise linear equation.
                            This equation is defined as:
                            _________________________________________

                                     Xn+1 = (aXn + c) mod m
                            _________________________________________

                            Change the initial 'seed' if you want
                            something else. This program does not
                            require any secure randomness, that is
                            becuase the random values only determine
                            the behavior of the particles.

    ARGUMENTS:
        - multiplier        int() 0 < 'a' < 'm'

        - increment         int() 0 <= 'c' < 'm'

        - modulus           int() 0 < 'm'

    RETURNS:
        - float()           Random value between 0 and 1
    """

    global seed

    # Linear congruention
    seed = (multiplier * seed + increment) % modulus

    return seed / modulus


def uniform(low, high):
    """
    Generate a random value between low and high

    NOTE:                   low <= high

    ARGUMENTS:
        - low               float() Eg, '-0.89'

        - high              float() Eg, '8.23'

    RETURNS:
        - float()           low <= float() <= high
    """

    return abs(high-low) * random() + low


def ndistance(p1, p2):
    """
    Calculate eucleidian distance between two points in N-dimensional space

    NOTE:                   The two points must have the same number of
                            dimensions, thus having the same shape.
                            Points' dimension is the same as their index.
                            Eg, point a: (2, 4) has two dimensions.

    ARGUMENTS:
        - p1                list() Coordinates. Eg, [0.2, 4, ..., n-1, n]

        - p2                list() Coordinates. Eg, [2, -7, ..., n-1, n]

    RETURNS:
        - float()           Eucledidian distance between both points.
    """

    return sum([(p1[i] - p2[i])**2 for i in range(len(p1))])**0.5


def nonlinear_rectifier(x0, x, x1):
    """
    Non-Linear Rectifier (LCR)

    NOTE:                   A non-linear rectifier (LCR) is
                            an algorithm that yields a input-value
                            rectified between two other values calculated
                            by relative distance. This equation is defined as:
                            ________________________________________________

                                         x1 - x0
                               --------------------------- + x0
                                      -e*(2x - (x1 + x0))
                                1 + e     --------------
                                             (x1 - x0)

                            ________________________________________________

                            If x is not between x0 and x1, x will be valued
                            closest to that value. This will create.
                            If x0<x<x1, x will kind of keep its value apart
                            from minor changes. If not x0<x<x1, x will be
                            fit within boundaries. It is bascically the
                            sigmoid function, but instead of: x -> 0<x<1
                            it is: x -> x0<x<x1

    ARGUMENTS:
        - x0                float() x0<x1

        - x                 float() The value to rectifiy.

        - x1                float() x0<x1

    RETURNS:
        - float()           x0<x<x1

    TODO:
    desmos.com:
    \frac{b-a}{1+e^{-e\cdot\frac{2x-\left(b+a\right)}{\left(b-a\right)}}}+a
    """

    return (x1-x0) / (1 + e**-(e*(2*x-(x1+x0))/(x1-x0))) + x0


def optimize(function, *, domain: list(), target: "see documentation", n=25,
             dims=False, iters=100, convergence=0.001, vmax=0.1, personal=2.0,
             social=2.0, seed=None):
    """
    Optimize a function

    ARGUMENTS:
        - function          function() The function to optimize without calling
                            it just send the variable name. Eg, 'ackley' or a
                            1/x function called 'myfunc':

                            ```
                            def myfunc(x):
                                return 1 / x
                            ```

    KEYWORD ARGUMENTS:
        - target            What to look for. The program will try to find a
                            certain way to get as close to the specified
                            keyword argument as possible. If you wan't to find
                            which varibles leads to a result closest to eg,
                            0.6. Then specify target as 'target=0.6'. If you
                            want to find the extrema of a function you can call
                            either 'maximum' or 'minimum'.

        - domain            list() The search space of the function 'function'
                            to be optimized. N-directional search space for non
                            cartesian environments. If nothing else presented,
                            the system thinks first position is lower boundary,
                            and the second, the upper boundary. Eg, [-2, 4]

        - n                 int() How many particles/n_particles to utilize.
                            Eg, 25

        - dims              int() Number of dimensions in the function to
                            optimize. If left as 'None', the program will
                            look up the number of positional arguments in the
                            function to optimize; 'function' as following:

                            ```
                            def function(a, b, c, *args, **kwargs):
                                ...
                                return float()
                            ```

                            In this case, the program will think the function
                            has 3 dimensions, as of the three positional
                            arguments. If 'dims' is not 'None', the program
                            will populate the function as specified by the
                            user. Eg, 4

        - iters             int() Maximum number of iterrations. Eg, 100

        - convergence       float() Convergence value. Eg, 0.001

        - vmax              float() Maximum velocity value for particle.
                            Eg, 0.1

        - personal          float() Particle personal coefficient factor.
                            Eg, 2.0

        - social            float() Particle social coefficient factor.
                            Eg, 2.0

        - seed              float() Random seed for reproducibility.
                            Eg, 5.2123

    RETURNS:
        - coordinates       list() Global best coordinates. Eg, [0.31, 4.21]

        - best              float() The solution. Eg, -3.21
    """

    # Makes maximum velocity relative to search domain
    vmax *= abs(domain[1]-domain[0])

    if not seed:
        globals()["seed"] = e


    if not dims:
        # Neat way to find number of positional arguments in a function
        if function.__defaults__ is not None:
            dims = function.__code__.co_argcount - len(function.__defaults__)
        else:
            dims = function.__code__.co_argcount

    # Populate the swarm
    swarm = []

    for id in range(n):

        # Initialize velocity for particle
        velocity = [random()*vmax, ]*dims

        # Generate initial coordinates within the 'domain'
        coordinates = [uniform(*domain), ]*dims

        # Initial value from the particle's coordinates
        extreme = function(*coordinates)

        # Particle structure: [id, velocity, extreme, coordinates, best]
        swarm.append([id, velocity, extreme, coordinates, coordinates.copy()])

    # What would later be the best particle, but for now just the last one
    coordinates = swarm[-1][3].copy()

    # What would later be the initial target, but for now just the last one
    best = swarm[-1][2]

    # Start of optimization
    for step in range(iters):

        distance_from_global_best = 0

        for particle in swarm:

            # Calculation for each dimension
            for i in range(len(particle[3])):
                # Update particle's dimensional velocity
                personal_coefficient = personal * random() * (particle[4][i] - particle[3][i])
                social_coefficient = social * random() * (coordinates[i] - particle[3][i])
                # Calculate new velocity
                inertia = uniform(0.5, 1.0)
                new_velocity = inertia * particle[1][i] + personal_coefficient + social_coefficient

                particle[1][i] = nonlinear_rectifier(-vmax, new_velocity, vmax)

                particle[3][i] += particle[1][i]

                # Update particle position to fit boundaries
                particle[3][i] = nonlinear_rectifier(domain[0], particle[3][i], domain[1])


            # Optimize for solution to 'function'
            particle[2] = function(*particle[3])

            # Update particle's best local position
            if target == 'minimum':
                if particle[2] < function(*particle[4]):
                    particle[4] = particle[3].copy()

                    if particle[2] < best:
                        # Update swarm's best global position
                        coordinates = particle[3].copy()
                        best = particle[2]

            elif target == 'maximum':
                if particle[2] > function(*particle[4]):
                    particle[4] = particle[3].copy()

                    if particle[2] > best:
                        # Update swarm's best global position
                        coordinates = particle[3].copy()
                        best = particle[2]

            elif target == int or float:
                # Find if current position is closer to target than local best
                if abs(particle[2]-target) < abs(function(*particle[4])-target):
                    particle[4] = particle[3].copy()

                    # Find if position is closer to target than global best
                    if abs(particle[2]-target) < abs(best-target):
                        coordinates = particle[3].copy()
                        best = particle[2]

            else:
                break

            # Calculate eucleidian distance between the particle's position
            # and global best
            distance_from_global_best += ndistance(particle[3], coordinates)

        # Convergence check, and break loop if satisfied
        if abs(best - distance_from_global_best) < convergence:
            break

    return coordinates, best
