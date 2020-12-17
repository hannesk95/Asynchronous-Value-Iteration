import numpy as np
import tqdm
import math
from numpy import linalg as LA


def state_to_tuple(x, n_stars):
    # Fuel f, goal star g and current node in graph i
    f = x // (n_stars * n_stars)
    g = x % (n_stars * n_stars) // n_stars
    i = x % (n_stars * n_stars) % n_stars

    return f, g, i


def state_from_tuple(f, g, i, n_stars):
    """ Fuel f, goal star g and current node in graph i """
    return f * n_stars * n_stars + g * n_stars + i


def one_step_cost(state, control, n_stars):
    f, g, i = state_to_tuple(state, n_stars)

    # In goal and no jump
    if g == i and control == 0:
        return -100.0

    # Out of fuel
    if f == 0:
        return 100.0

    # Avoid unnecessary jumps
    if control > 0:
        return 5.0

    # Else no cost
    return 0.0


def iterate(t_prob, J_star, epsilon, alpha, max_u, n_stars, max_f):

    J = np.zeros(t_prob.shape[1])
    pi = np.zeros(t_prob.shape[1])
    error = math.inf

    #while error > epsilon:
    for _ in range(10):
        for state in range(t_prob.shape[1]):
            J_temp = []
            t_prob_temp = t_prob[state * max_u: state * max_u + max_u, :]

            for action in range(max_u):
                t_prob_current = t_prob_temp[action, :]
                idx = np.nonzero(t_prob_current)[0]

                if len(idx) == 0:
                    continue

                else:
                    cost = one_step_cost(state, action, n_stars)
                    J_temp.append((t_prob_current.multiply(cost + alpha * J).toarray()).sum())

            J[state] = np.min(J_temp)
            pi[state] = np.argmin(J_temp)

        error = LA.norm(J - J_star)

    return J, pi
