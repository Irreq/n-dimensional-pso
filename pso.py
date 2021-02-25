#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pso.py
#
# Author : Irreq
#
# DOCUMENTATION:
#
# See: 'README.md' or read comments in functions

seed = 2.718281828459045235360287471352662497757

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
        - multiplier        int() 0 < a < m

        - increment         int() 0 <= c < m

        - modulus           int() 0 < m

    """

    global seed

    # Linear congruention
    seed = (multiplier * seed + increment) % modulus

    return seed / modulus

def uniform(low, high):

    """
    Generate a random value between low and high

    ARGUMENTS:
        - low               float() Eg, '-0.89'

        - high              float() Eg, '8.23'
    """

    return abs(high-low) * random() + low

def ndistance(p1, p2):

    """
    Calculate eucleidian distance between
    two points in N-dimensional space
    """

    return sum([(p1[i] - p2[i])**2 for i in range(len(p1))])**0.5

def optimize(function, *, domain: list(), target: "see documentation", n=25, dims=False, iters=100, convergence=0.001, vmax=0.1, personal=2.0, social=2.0) -> random():

    """
    Omni Dimensional Particle Swarm Optimization without external libraries (RAW Python)

    DOCUMENTATION:          Read this or see: 'README.md' or read comments in functions

    ARGUMENTS:
        - function          function() The function to optimize without calling it just send the
                            variable name. Eg, 'ackley'

    KEYWORD ARGUMENTS:
        - target            What to look for. The program will try to find a certain way to get as close
                            to the specified keyword argument as possible. If you wan't to find which varibles
                            leads to a result closest to eg, 0.6. Then specify target as 'target=0.6'. If you want
                            to find the extrema of a function you can call either 'maximum' or 'minimum'.

        - domain            list() The search space of the function 'function' to be optimized. N-directional search
                            space for non cartesian environments. If nothing else presented, the system thinks first
                            position is lower boundary, and the second, the upper boundary. Eg, [-2, 4]

        - n                 int() How many particles/n_particles to utilize. Eg, 25

        - dims              int() Number of dimensions in the function to optimize. If left as 'None', the program will
                            look up the number of positional arguments in the function to optimize; 'function' as following:

                            def function(a, b, c, *args, **kwargs):
                                ...
                                return int()

                            In this case, the program will think the function has 3 dimensions, as of the three positional arguments
                            If dims is not 'None', the program will populate the function as specified by the user. Eg, 4

        - iters             int() Maximum number of iterrations. Eg, 100

        - convergence       float() Convergence value. Eg, 0.001

        - vmax              float() Maximum velocity value for particle. Eg, 0.1

        - personal          float() Particle personal coefficient factor. Eg, 2.0

        - social            float() Particle social coefficient factor. Eg, 2.0

    TODO:                   Finnish documentation
                            + the dancers and killers.
                            - dead code.
    """

    if not dims:
        # Neat way to find number of positional arguments in a function
        dims = function.__code__.co_argcount - len(function.__defaults__) if function.__defaults__ != None else function.__code__.co_argcount

    # Populate the swarm
    swarm = []

    for id in range(n):

        # Initialize velocity for particle
        velocity = [random()*vmax,]*dims

        # Generate initial coordinates within the 'domain'
        coordinates = [uniform(*domain),]*dims

        # Initial value from the particle's coordinates
        extreme = function(*coordinates)

        # Particle structure: [id, velocity, extreme, coordinates, best]
        swarm.append([id, velocity, extreme, coordinates, coordinates.copy()])


    # What would later be the best particle, but for now just the last one
    coordinates = swarm[-1][3].copy()

    # What would later be the initial target, but for now just the last one
    best = swarm[-1][2]

    for step in range(iters):

        distance_from_global_best = 0

        for particle in range(len(swarm)):

            # Calculation for each dimension
            for i in range(len(swarm[particle][3])):
                # Update swarm[particle]'s dimensional velocity
                personal_coefficient = personal * random() * (swarm[particle][4][i] - swarm[particle][3][i])
                social_coefficient = social * random() * (coordinates[i] - swarm[particle][3][i])
                # Calculate new velocity
                inertia = uniform(0.5, 1.0)
                new_velocity = inertia * swarm[particle][1][i] + personal_coefficient + social_coefficient

                # Check if velocity is exceeded
                if new_velocity > vmax:
                    swarm[particle][1][i] = vmax

                elif new_velocity < -vmax:
                    swarm[particle][1][i] = -vmax

                else:
                    swarm[particle][1][i] = new_velocity

                swarm[particle][3][i] += swarm[particle][1][i]

                # Update swarm[particle] position to fit boundaries
                if not domain[0] < swarm[particle][3][i] < domain[1]: # FIX THIS FOR MULTI DOMAINS
                    swarm[particle][3][i] = uniform(domain[0], domain[1])

            # Optimize for solution to 'function'
            swarm[particle][2] = function(*swarm[particle][3])

            # Update swarm[particle]'s best local position
            if target == 'minimum':
                if swarm[particle][2] < function(*swarm[particle][4]):
                    swarm[particle][4] = swarm[particle][3].copy()

                    if swarm[particle][2] < best:
                        # Update swarm's best global position
                        coordinates = swarm[particle][3].copy()
                        best = swarm[particle][2]

            elif target == 'maximum':
                if swarm[particle][2] > function(*swarm[particle][4]):
                    swarm[particle][4] = swarm[particle][3].copy()

                    if swarm[particle][2] > best:
                        # Update swarm's best global position
                        coordinates = swarm[particle][3].copy()
                        best = swarm[particle][2]

            elif target == int or float:

                # Find if current position is closer to target than local best
                if abs(swarm[particle][2]-target) < abs(function(*swarm[particle][4])-target):
                    swarm[particle][4] = swarm[particle][3].copy()

                    # Find if current position is closer to target than global best
                    if abs(swarm[particle][2]-target) < abs(best-target):
                        coordinates = swarm[particle][3].copy()
                        best = swarm[particle][2]

            # Calculate the eucleidian distance between the particle's position and the global best position
            distance_from_global_best += ndistance(swarm[particle][3], coordinates)

        # Convergence check, and break loop if satisfied
        if abs(best - distance_from_global_best) < convergence:
            break

    return coordinates, best
