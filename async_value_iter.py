import time
import pickle
import numpy as np
import scipy.sparse
import matplotlib.pyplot as plt

from backend import *

def load_sparse_matrix(data_dir, name):
    indptr = np.load(f"{data_dir}/{name}_indptr.npy")
    indices = np.load(f"{data_dir}/{name}_indices.npy")
    data = np.load(f"{data_dir}/{name}_data.npy")
    shape = np.load(f"{data_dir}/{name}_shape.npy")
    return data, indices, indptr, shape

def to_sparse_matrix(data, indices, indptr, shape):
    # Eigen provides a similar why to create a CSR view of these arrays, take a look at Eigen::Map< CSR Matrix >(...)
    return scipy.sparse.csr_matrix((data, indices, indptr), shape=shape, dtype=data.dtype)

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

    # error = math.inf
    J = np.zeros(t_prob.shape[1])
    pi = np.zeros(t_prob.shape[1])

    epsilon = 10e-1     # Maximum error margin
    alpha = 0.99        # Discount factor

    t1 = time.perf_counter()

    #J_final, pi_final = backend.iterate(t_prob, J_star, J, pi, epsilon, alpha, max_u, n_stars, max_f)

    t2 = time.perf_counter()

    J_final, pi_final = backend_py.iterate(t_prob, J_star, J, pi, epsilon, alpha, max_u, n_stars, max_f)

    t3 = time.perf_counter()

    print(f"C++ took {t2 - t1} seconds")
    print(f"Python took {t3 - t2} seconds")

    # Plotting
    plt.figure()
    plt.title("Optimal Path")


    plt.grid()
    plt.plot()


if __name__ == "__main__":
    main()
