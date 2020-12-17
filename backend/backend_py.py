import numpy as np

class Parameters:
  k = 0.99  # Dampening of velocity
  v_max = 0.5  # Max speed to prevent explosions
  x_max = 1.5  # Half size of the world

  m = 5e4  # Mass of particles, somewhat large to compensate the force
  G = 6.6743e-11  # Gravity constant in m^3 / (kg s^2)

def gravity(x1, x2):
  """ Returns the force acting on x1. x2 receives the same force with different sign. """
  d = x2 - x1
  r = np.linalg.norm(d)
  d /= r
  f = Parameters.G * Parameters.m * Parameters.m / (r * r)
  return f * d

def simulate(x, v, dt=1e-1):

  N = x.shape[1]

  F = np.zeros_like(x)

  for p1 in range(N):
    for p2 in range(p1 + 1, N):
      f = gravity(x[p1, :], x[p2, :])
      F[p1, :] += f
      F[p2, :] -= f

  # Simple euler step
  v = Parameters.k * v + dt * F / Parameters.m
  v = np.clip(v, -Parameters.v_max, Parameters.v_max)

  x = x + dt * v
  x = np.clip(x, -Parameters.x_max, Parameters.x_max)

  return x, v

def simulate_T_steps(x, v, dt=1e-1, T=100):
  for t in range(T):
    x, v = simulate(x, v, dt)
  return x, v

if __name__ == "__main__":
  from matplotlib import pyplot as plt

  plt.figure()
  r = np.linspace(0.1, 2, 1000)
  plt.plot(r, -Parameters.G * Parameters.m ** 2 / r ** 2)
  plt.xlabel("r")
  plt.ylabel("f")
  plt.grid()
  plt.show()
