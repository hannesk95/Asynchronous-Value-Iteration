import numpy as np
import tqdm
import math
from numpy import linalg as LA
import scipy.sparse


def state_to_tuple(x, n_stars):
    # Fuel f, goal star g and current node in graph i
    f = x // (n_stars * n_stars)
    g = x % (n_stars * n_stars) // n_stars
    i = x % (n_stars * n_stars) % n_stars

    return f, g, i


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


def to_sparse_matrix(data, indices, indptr, shape):
    # Eigen provides a similar why to create a CSR view of these arrays, take a look at Eigen::Map< CSR Matrix >(...)
    return scipy.sparse.csr_matrix((data, indices, indptr), shape=shape, dtype=data.dtype)


def iterate(data, indices, indptr, n_rows, n_columns,
            J_star, J, pi, epsilon, alpha, n_actions,
            n_stars, n_states):

    t_prob = to_sparse_matrix(data, indices, indptr, (n_rows, n_columns))

    error = math.inf

    while error > epsilon:
    # for _ in range(1000):
        for state in range(n_states):
            J_temp = []
            t_prob_temp = t_prob[state * n_actions: state * n_actions + n_actions, :]

            for action in range(n_actions):
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
