import numpy as np

import pytest

from backend import *

def test_cpp_backend_active():
  """ Tests, whether the C++ backend is running """
  assert backend is not backend_py, "The C++ Backend is not active, you are testing the functions with themself!"
  return

def test_simulate():
  """ Tests, whether the simulate steps matches between Python and C++ """

  #             ^
  #        ->   |   <-
  # -------x----+----x-------->
  #  Particle 1 | Particle 2
  #             |

  x = np.array([[-1.0, 0.0],
                [1.0, 0.0]], dtype=np.double)
  v = np.array([[0.1, 0.0],
                [-0.1, 0.0]], dtype=np.double)

  # Copy to avoid call by reference issue
  x_py, v_py = backend_py.simulate(x.copy(), v.copy(), 0.5)
  x_cpp, v_cpp = backend.simulate(x.copy(), v.copy(), 0.5)

  assert np.allclose(x_py, x_cpp), "Position missmatch between C++ and Python code."
  assert np.allclose(v_py, v_cpp), "Velocity missmatch between C++ and Python code."

  return
