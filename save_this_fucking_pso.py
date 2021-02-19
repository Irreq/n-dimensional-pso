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

                            change the initial 'seed' if you want
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

    difference = abs(low - high)
    return (random() * difference) + difference

def ndistance(p1, p2):

    """
    Calculate eucleidian distance between
    two points in N-dimensional space
    """

    return sum([(p1[i] - p2[i])**2 for i in range(len(p1))])**0.5


class Swarm():

    def __init__(self, function, agents, vmax, dims, domain, extrema):
        """
        Swarm Generation

        NOTE:                   This class should not be called by
                                the user, its is recomended to use
                                the 'PSO' class.

        ARGUMENTS:
            - function          function() The function to optimize.
                                Eg, 'ackley'

            - agents            int() Number of particles in the
                                optimization. Eg, 25

            - vmax              float() Maximum velocity value for
                                particle. Eg, 0.1

            - dims              int() Number of dimensions in the function to
                                optimize. If left as 'None', the program will
                                look up the number of positional arguments in
                                the function to optimize; 'function' as following:

                                def function(a, b, c, *args, **kwargs):
                                    ...
                                    return int()

                                In this case, the program will think the function
                                has 3 dimensions, as of the three positional arguments
                                If dims is not 'None', the program will populate the
                                function as specified by the user. Eg, 4

            - domain            list() The search space of the function 'function' to be
                                optimized. N-directional search space for non cartesian
                                environments. If nothing else presented, the system
                                thinks first position is lower boundary, and the
                                second, the upper boundary. Eg, [-2, 4]

            - extrema           string() What to look for. Either 'maximum'
                                or 'minimum'.


        """
        self.particles = []       # All particles
        self.best = None          # Best particle
        self.extreme = 0          # Initial extrema

        for i in range(agents):

            # Generate initial coordinates within the 'domain'
            coordinates = [uniform(*domain),]*dims

            # Initial value from the particle's coordinates
            extreme = function(*coordinates)

            # Initialize velocity for particle
            velocity = [random()*vmax,]*dims

            # Generate particle
            particle = self.Particle(velocity, extreme, coordinates)
            self.particles.append(particle)

            if self.best != None:

                if extrema == 'minimum':
                    if particle.extreme < self.extreme:
                        self.best = particle.position.copy()
                        self.extreme = particle.extreme

                if extrema == 'maximum':
                    if particle.extreme > self.extreme:
                        self.best = particle.position.copy()
                        self.extreme = particle.extreme

            else:
                # First iteration
                self.best = particle.position.copy()
                self.extreme = particle.extreme

    # Particle subclass
    class Particle():

        def __init__(obj, velocity, extreme, coordinates):

            """
            These are the attributes assigned to each worker particle/agent

            NOTE:                   This class should not be called by
                                    the user, its is recomended to use
                                    the 'PSO' class.

            ARGUMENTS:
                - velocity          list() N-dimensional list
                                    containing each directional speed.
                                    Eg, [0.12, 0.88]

                - extreme           float() Value for the particle's
                                    current position. Eg, '0.23'

                - *coordinates
            """

            obj.velocity = velocity            # Particle velocity
            obj.extreme = extreme              # Particle value on current position
            obj.position = coordinates         # Particle coordinates
            obj.best = obj.position.copy()     # The best position


class PSO():

    def __init__(self, *, agents: int(), dims=None, iters=100, convergence=0.001, vmax=0.1, personal=2.0, social=2.0, global_best=0.0, initialseed=None):


        """
        Omni Dimensional Particle Swarm Optimization without external libraries (RAW Python)

        Note:                   PSO, particle swarm optimization.

        KEYWORD ARGUMENTS:
            - agents            int() How many particles/agents to utilize.
                                Eg, 25

            - dims              int() Number of dimensions in the function to
                                optimize. If left as 'None', the program will
                                look up the number of positional arguments in
                                the function to optimize; 'function' as following:

                                def function(a, b, c, *args, **kwargs):
                                    ...
                                    return int()

                                In this case, the program will think the function
                                has 3 dimensions, as of the three positional arguments
                                If dims is not 'None', the program will populate the
                                function as specified by the user. Eg, 4

            - iters         int() Maximum number of iterrations.
                                Eg, 100

            - convergence       float() Convergence value. Eg, 0.001

            - vmax              float() Maximum velocity value for
                                particle. Eg, 0.1

            - personal          float() Particle personal coefficient factor.
                                Eg, 2.0

            - social            float() Particle social coefficient factor.
                                Eg, 2.0

            - global_best       float() Global best of the function: 'function'.
                                Eg, 0.0

            - initialbest       int() Seed for the randomizing function.
                                Eg, '231234442'

        TODO:                   Finnish documentation
                                + minimum gang and maximum gang.
                                + the dancers and killers.
                                - dead code.
        """

        # Initialize some random variables
        global seed
        if initialseed != None:
            seed = initialseed

        for _ in range(1000):
            random()

        self.agents = agents
        self.dims = dims

        self.iters = iters
        self.convergence = convergence
        self.vmax = vmax
        self.personal = personal
        self.social = social
        self.global_best = global_best

        self.inertia = 0.5 + random() / 2

        self.iterations = 0
        self.running = True

        self.function = None
        self.extrema = None
        self.domain = None
        self.swarm = []



    def optimize(self, function, extrema, *, domain: list()):

        """
        Initializing function for optimization.

        Note:                   None

        ARGUMENTS:
            - function          function() The function to optimize.
                                Eg, 'ackley'

            - extrema           string() What to look for. Either 'maximum'
                                or 'minimum'.

        KEYWORD ARGUMENTS:
            - domain            list() The search space of the function 'function' to be
                                optimized. N-directional search space for non cartesian
                                environments. If nothing else presented, the system
                                thinks first position is lower boundary, and the
                                second, the upper boundary. Eg, [-2, 4]

        TODO:                   Clean up code.

        """

        self.distribution = []
        self.avgbest = []

        self.running = True
        assert extrema in ['maximum', 'minimum']

        if self.dims == None:
            self.dims = function.__code__.co_argcount - len(function.__defaults__) if function.__defaults__ != None else function.__code__.co_argcount

        assert 0 < self.dims and type(self.dims) == int, "You must use integer dimensions"

        self.function = function
        self.extrema = extrema
        self.domain = domain
        # Initialize swarm
        self.swarm = Swarm(self.function, self.agents, self.vmax, self.dims, self.domain, self.extrema)

        while self.iterations < self.iters and self.running:
            self.next()

        return self.swarm.extreme, self.swarm.best


    def movement(self, particle):

        """
        Calculation for every dimension in the particle.
        """

        for i in range(len(particle.position)):

            # Update particle's dimensional velocity
            personal_coefficient = self.personal * random() * (particle.best[i] - particle.position[i])
            social_coefficient = self.social * random() * (self.swarm.best[i] - particle.position[i])
            new_velocity = self.inertia * particle.velocity[i] + personal_coefficient + social_coefficient

            # Check if velocity is exceeded
            if new_velocity > self.vmax:
                particle.velocity[i] = self.vmax

            elif new_velocity < -self.vmax:
                particle.velocity[i] = -self.vmax

            else:
                particle.velocity[i] = new_velocity

            particle.position[i] += particle.velocity[i]

            # Update particle position to fit boundaries
            if not self.domain[0] < particle.position[i] < self.domain[1]:
                particle.position[i] = uniform(self.domain[0], self.domain[1])

        # Optimize for solution to 'function'
        particle.extreme = self.function(*particle.position)

        # Update particle's best local position
        if self.extrema == 'minimum':
            if particle.extreme < self.function(*particle.best):
                particle.best = particle.position.copy()

                if particle.extreme < self.swarm.extreme:
                    # Update swarm's best global position
                    self.swarm.best = particle.position.copy()
                    self.swarm.extreme = particle.extreme

        if self.extrema == 'maximum':
            if particle.extreme > self.function(*particle.best):
                particle.best = particle.position.copy()

                if particle.extreme > swarm.extreme:
                    # Update swarm's best global position
                    self.swarm.best = particle.position.copy()
                    self.swarm.extreme = particle.extreme

        self.distance_from_global_best += ndistance(particle.position, self.swarm.best)

    def next(self):

        """
        Each step in the optimization.
        The code finish if it meets convergence.
        """

        self.distance_from_global_best = 0

        for particle in self.swarm.particles:
            self.movement(particle)

        self.distribution.append(self.distance_from_global_best / self.agents)
        self.avgbest.append(self.swarm.extreme)

        # Convergence check, and break loop if satisfied
        if abs(self.swarm.extreme - self.global_best) < self.convergence:
            self.running = False

        self.iterations += 1
