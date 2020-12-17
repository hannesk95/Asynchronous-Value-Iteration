import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
import scipy.sparse
import pickle
import math
from numpy import linalg as LA
from tqdm import tqdm

def load_sparse_matrix(data_dir, name):
    indptr = np.load(f"{data_dir}/{name}_indptr.npy")
    indices = np.load(f"{data_dir}/{name}_indices.npy")
    data = np.load(f"{data_dir}/{name}_data.npy")
    shape = np.load(f"{data_dir}/{name}_shape.npy")
    return data, indices, indptr, shape


def to_sparse_matrix(data, indices, indptr, shape):
    # Eigen provides a similar why to create a CSR view of these arrays, take a look at Eigen::Map< CSR Matrix >(...)
    return scipy.sparse.csr_matrix((data, indices, indptr), shape=shape, dtype=data.dtype)


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


def main():
    data_dir = "data/data_debug"
    t_prob = to_sparse_matrix(*load_sparse_matrix(data_dir, "P"))
    J_star = np.load(f"{data_dir}/J_star_alpha_0_99_iter_1000.npy")
    pi_star = np.load(f"{data_dir}/pi_star_alpha_0_99_iter_1000.npy")

    with open(f"{data_dir}/parameters.pickle", "rb") as the_file:
        parameters = pickle.load(the_file)

    max_u = parameters["max_controls"]
    n_stars = parameters["number_stars"]
    max_f = parameters["fuel_capacity"]

    error = math.inf
    epsilon = 10e-5
    alpha = 0.99
    J = np.zeros(t_prob.shape[1])
    pi = np.zeros(t_prob.shape[1])

    # while error > epsilon:
    for _ in tqdm(range(1000)):
      for state in range(t_prob.shape[1]):
        J_temp = []
        t_prob_temp = t_prob[state*(max_u):state*(max_u)+max_u, :]

        for action in range(max_u):
            t_prob_current = t_prob_temp[action, :]
            idx = np.nonzero(t_prob_current)[0]

            if len(idx) == 0:
                continue

            # elif len(idx) >= 1:
            #     current_state = state_from_tuple(max_f - 1,  # Start with max fuel
            #                                   n_stars - 1,  # Goal is last star
            #                                   0,  # Start is the star with label 0
            #                                   n_stars)
            #     cost = one_step_cost(state, action, n_stars)
            #     #J_temp.append(cost + alpha * J[idx])
            #     J_temp.append((t_prob_current.multiply(cost + alpha * J).toarray()).sum())

            else:
                # current_state = state_from_tuple(max_f - 1,  # Start with max fuel
                #                               n_stars - 1,  # Goal is last star
                #                               0,  # Start is the star with label 0
                #                               n_stars)
                cost = one_step_cost(state, action, n_stars)

                J_temp.append((t_prob_current.multiply(cost + alpha * J).toarray()).sum())
                #J_temp.append(np.array(t_prob_current.multiply(cost + alpha * J)).sum())

        J[state] = np.min(J_temp)
        pi[state] = np.argmin(J_temp)


    print("\n Euclidean distance of J* to J: " + str(LA.norm(J - J_star)))
    print("\n Euclidean distance of pi* to pi: " + str(LA.norm(pi - pi_star)))

    with open('.data/data_debug/pi_own.npy', 'wb') as f:
        np.save(f, pi)

    with open('.data/data_debug/J_own.npy', 'wb') as f:
        np.save(f, J)

if __name__ == "__main__":
    main()
