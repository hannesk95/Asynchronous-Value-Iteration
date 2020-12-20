# %% Imports


import time
import numpy as np

from matplotlib import pyplot as plt

from backend import *

# %% Functions

def potential(r):
  """ Lennard Jones (12,6) Potential """
  eps = 1.0  # "Depth" of valley
  r_m = 1.25  # Position of valley

  foo = np.power(r_m / r, 6)
  return eps * foo * (foo - 2)

def force(r):
  eps = 1.0  # "Depth" of valley
  r_m = 1.25  # Position of valley

  foo = np.power(r_m / r, 6)
  return - 12.0 * eps / r * foo * (foo + 1)

# %% Working code

T = 25_000
N = 200

# Row Major format, each row is one particle to make use of continuous memory
x = np.random.uniform(-0.5 * backend_py.Parameters.x_max, 0.5 * backend_py.Parameters.x_max, size=(N, 2))
v = np.random.uniform(-0.1 * backend_py.Parameters.v_max, 0.1 * backend_py.Parameters.v_max, size=(N, 2))

# For debugging
# x = np.array([[0., 0.],
#               [1., 1.],
#               [-1., -1.]])
# v = np.zeros_like(x)

X = np.empty((T,) + x.shape)
V = np.empty_like(X)

X[0, ...] = x.copy()
V[0, ...] = v.copy()

t1 = time.perf_counter()

for t in range(T - 1):
  X[t + 1, ...], V[t + 1, ...] = backend.simulate(X[t, ...], V[t, ...])

t2 = time.perf_counter()

for t in range(T - 1):
  X[t + 1, ...], V[t + 1, ...] = backend_py.simulate(X[t, ...], V[t, ...])

t3 = time.perf_counter()

print(f"C++ took {t2 - t1} seconds")
print(f"Python took {t3 - t2} seconds")

# %% Plotting

plt.figure()
plt.title("x marks the start")

for n in range(N):
  plt.plot(X[0, n, 0], X[0, n, 1], 'kx')
  plt.plot(X[:, n, 0], X[:, n, 1], '-+')

plt.xlabel("x")
plt.ylabel("y")

# plt.xlim((-Parameters.x_max, Parameters.x_max))
# plt.ylim((-Parameters.x_max, Parameters.x_max))

plt.grid()
plt.show()
