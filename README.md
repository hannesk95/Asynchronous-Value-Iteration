# Dynamic-Programming using OpenMP in C++
---
### Preface

This project implements an asynchronous value iteration for a Markov Decisioin Process (MDP) using Bellman's principle of optimality. Python (for convenience purposes) and C++ (for performance purposes) are linked using [**CFFI**](https://cffi.readthedocs.io/en/latest/). Furthermore, [**OpenMP**](https://www.openmp.org//wp-content/uploads/OpenMP-4.0-C.pdf) is used in order to parallelize the iteration process. 

---

### Repository Structure

- [`backend`](/backend) includes the python module
- [`cpp_backend`](/cpp_backend) includes the C++ source code
- [`data`](/data) includes some example scipy spare matrix data
- [`tests`](/tests) includes scripts for PyTest

---

### Prerequisits for Linux Enviroment (Tested on Ubuntu 20.04)
- [Make](https://en.wikipedia.org/wiki/Make_(software)) - Build automation tool that automatically builds executable programs and libraries from source code by reading files called Makefiles

- [CMake](https://cmake.org/) - Platform for build automation, testing and packaging using a compiler-independent method
<br/> `sudo apt-get install cmake`
<br/> `sudo apt-get install build-essential`

- [Eigen](http://eigen.tuxfamily.org/index.php?title=Main_Page) - C++ template library for linear algebra
<br/> `sudo apt-get install libopenblas-dev` 
<br/> `sudo apt-get install liblapack-dev` 
<br/> `sudo apt-get install liblapacke-dev` 
<br/> `sudo apt-get install zlib1g-dev`
  
- [OpenMP](https://www.openmp.org/) - API specification for parallel programming
<br/> `sudo apt-get install openmpi-bin`
<br/> `sudo apt-get install openmpi-common`
<br/> `sudo apt-get install libopenmpi-dev`
  
---

### Execution

In order to make use of the code, please invoke the following steps:
1. Invoke following command in the root directory of this repository: `make compile`
2. Start application by invoking: `python3 main.py`

---

### Remarks

Thank's to [`Martin Gottwald`](https://www.ei.tum.de/ldv/team/wissenschaftliche-mitarbeiter/martin-gottwald/) for kindly providing the interface part (Python/C++) using CFFI. 
