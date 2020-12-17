import numpy as np

data_dir = "data_debug"

J_star = np.load(f"{data_dir}/J_star_alpha_0_99_iter_1000.npy")
pi_star = np.load(f"{data_dir}/pi_star_alpha_0_99_iter_1000.npy")
J = np.load(f"{data_dir}/J_own.npy")
pi = np.load(f"{data_dir}/pi_own.npy")



print("Hello")