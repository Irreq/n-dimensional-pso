import numpy as np

from pso import optimize

# Famous computer optimization benchmark algorithm
def ackley(x, y, a=20, b=0.2, c=2*np.pi):

    term_1 = np.exp((-b * np.sqrt(0.5 * (x ** 2 + y ** 2))))
    term_2 = np.exp((np.cos(c * x) + np.cos(c * y)) / 2)
    return -1 * a * term_1 - term_2 + a + np.exp(1)

def sin(x):
    return np.sin(x)

def cos(x):
    return np.cos(x)

def sawtooth(x):
    return abs(x)

def foo(x):

    return abs(2*x**2-3*x**6) + np.sin(x)

if __name__ == "__main__":

    # Lets find the optimized function in this domain
    SEARCH_SPACE = [np.pi, 2*np.pi]

    # Number of particles who will try to optimize the function
    N = 30

    # It is suggested to run several optimizations to get a mean.
    # The PSO optimization is prone to noticable fluctuations in the results
    # due to its pseudo-random nature
    # pso = PSO(agents=N)

    optimizer = optimize(sin, 'minimum', domain=SEARCH_SPACE)

    # print(pso.swarm.extreme, pso.swarm.best)

    print(optimizer.swarm.best[-1]/np.pi)

    optimizer = PSO(particles=N)

    optizer.optimize(cos, 'max', domain=[0.8, 3*np.pi])

    value, coordinates = optimizer.best
