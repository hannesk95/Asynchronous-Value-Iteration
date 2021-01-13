## Asynchronous-Value-Iteration

This project implements an asynchronous value iteration for a Markov Decisioin Process (MDP). Python (for convenience purposes) and C++ (for performance purposes) are linked using [**CFFI**](https://cffi.readthedocs.io/en/latest/). Furthermore, **OpenMP** is used in order to parallelize the iteration process. 

- `backend` includes the python module
- `cpp_backend` includes the C++ source code
- `tests` includes scripts for PyTest
- `data` includes some example scipy spare matrix data
