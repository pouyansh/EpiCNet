from numpy import random as rd


# This method returns a value from the normal distribution with mean=p and standard deviation=std
def calculate_normal(p):
    result = rd.normal(loc=p, scale=0.1 * p, size=1)[0]
    while result < 0:
        result = rd.normal(loc=p, scale=0.1 * p, size=1)[0]
    return result


# This method returns a value based on the binomial distribution
def calculate_binomial(p, n):
    return rd.binomial(n, p)
