import time
import pickle
import numpy as np
import numpy.linalg
from backend import *


def main():
    data_dir = "data/data_debug"    # Set data directory here
    epsilon = 10e-5                 # Set maximum error margin here
    alpha = 0.99                    # Set discount factor here

    # Load reference data
    data = np.load(f"{data_dir}/P_data.npy")
    indices = np.load(f"{data_dir}/P_indices.npy")
    indptr = np.load(f"{data_dir}/P_indptr.npy")
    shape = np.load(f"{data_dir}/P_shape.npy")
    J_star = np.load(f"{data_dir}/J_star_alpha_0_99_iter_1000.npy")
    pi_star = np.load(f"{data_dir}/pi_star_alpha_0_99_iter_1000.npy")

    with open(f"{data_dir}/parameters.pickle", "rb") as the_file:
        parameters = pickle.load(the_file)

    # Define useful variables
    n_rows = shape[0]
    n_columns = shape[1]
    n_actions = parameters["max_controls"]
    n_stars = parameters["number_stars"]
    n_fuel = parameters["fuel_capacity"]
    n_states = n_stars * n_stars * n_fuel
    n_nonzero = len(data)

    # Variables which serve as data storage for C++ part
    J = np.ones(shape[1])
    pi = np.ones(shape[1])

    print("\n Start C++ code \n")
    t1 = time.perf_counter()

    # Invoke C++ backend
    J_cpp, pi_cpp = backend.iterate(data, indices, indptr, n_rows, n_columns,
                                    J_star, J, pi, epsilon, alpha, n_actions,
                                    n_stars, n_states, n_nonzero)

    print("End C++ code \n")
    t2 = time.perf_counter()
    # print("\n Start Python code \n")
    #
    # # Invoke Python backend
    # J_py, pi_py = backend_py.iterate(data, indices, indptr, n_rows, n_columns,
    #                                  J_star, J, pi, epsilon, alpha, n_actions,
    #                                  n_stars, n_states, n_nonzero)
    #
    # t3 = time.perf_counter()
    # print("End Python code \n")
    #
    # # Compare results of both backends
    # if np.allclose(J_py, J_cpp):
    #     print("J_py and J_cpp are equal!")

    print(f"C++ took {t2 - t1} seconds")
    # print(f"Python took {t3 - t2} seconds")
    # print(f"Distance J_py and J_cpp: {numpy.linalg.norm(J_cpp - J)}")
    # print(f"Python distance J* and J: {numpy.linalg.norm(J_star - J)}")
    # print(f"Python distance pi* and pi: {numpy.linalg.norm(pi_star - pi)}")
    print("Jstar" + str(J_star))
    print("Jcpp" + str(J_cpp))



if __name__ == "__main__":
    main()
