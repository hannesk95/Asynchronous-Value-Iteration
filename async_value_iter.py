import time
import pickle
import numpy as np
import scipy.sparse
import matplotlib.pyplot as plt
import numpy.linalg as LA
from backend import *

# def load_sparse_matrix(data_dir, name):
#     indptr = np.load(f"{data_dir}/{name}_indptr.npy")
#     indices = np.load(f"{data_dir}/{name}_indices.npy")
#     data = np.load(f"{data_dir}/{name}_data.npy")
#     shape = np.load(f"{data_dir}/{name}_shape.npy")
#     return data, indices, indptr, shape

# def to_sparse_matrix(data, indices, indptr, shape):
#     # Eigen provides a similar why to create a CSR view of these arrays, take a look at Eigen::Map< CSR Matrix >(...)
#     return scipy.sparse.csr_matrix((data, indices, indptr), shape=shape, dtype=data.dtype)

def main():

    data_dir = "data/data_debug"    # Set data directory here
    epsilon = 10e-1                 # Set maximum error margin here
    alpha = 0.99                    # Set discount factor here

    data = np.load(f"{data_dir}/P_data.npy")
    indices = np.load(f"{data_dir}/P_indices.npy")
    indptr = np.load(f"{data_dir}/P_indptr.npy")
    shape = np.load(f"{data_dir}/P_shape.npy")
    J_star = np.load(f"{data_dir}/J_star_alpha_0_99_iter_1000.npy")
    print(f"{J_star}")
    pi_star = np.load(f"{data_dir}/pi_star_alpha_0_99_iter_1000.npy")

    with open(f"{data_dir}/parameters.pickle", "rb") as the_file:
        parameters = pickle.load(the_file)

    n_rows = shape[0]
    n_columns = shape[1]
    n_actions = parameters["max_controls"]
    n_stars = parameters["number_stars"]
    n_fuel = parameters["fuel_capacity"]
    n_states = n_stars * n_stars * n_fuel

    J = np.zeros(shape[1])
    pi = np.zeros(shape[1])

    t1 = time.perf_counter()

    # J_final, pi_final = backend.iterate(t_prob, J_star, J, pi, epsilon, alpha, max_u, n_stars, max_f)

    t2 = time.perf_counter()

    # J_final, pi_final = backend_py.iterate(t_prob, J_star, J, pi, epsilon, alpha, max_u, n_stars, max_f)
    J_final, pi_final = backend_py.iterate(data, indices, indptr, n_rows, n_columns,
                                           J_star, J, pi, epsilon, alpha, n_actions,
                                           n_stars, n_states)

    t3 = time.perf_counter()

    print(f"C++ took {t2 - t1} seconds")
    print(f"Python took {t3 - t2} seconds")
    print(f"Python distance J* and J: {LA.norm(J_star - J_final)}")

    # Plotting
    plt.figure()
    plt.title("Optimal Path")


    plt.grid()
    plt.plot()


if __name__ == "__main__":
    main()
