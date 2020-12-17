#include "Simulator.h"

// Interface C code for CFFI ...
extern "C"
{
  extern void cffi_simulate(double* x, double* v,
                            const unsigned int N, const unsigned int dim,
                            const double dt)
  {
    // No C++ in here, but namespaces work in external C linkage
    // But only from C++ -> C direction, don't try to define new namespaces inside this C realm
    Backend::simulate(x, v, N, dim, dt);
  }

  extern void cffi_simulate_T_steps(double* x, double* v,
                                    const unsigned int N, const unsigned int dim,
                                    const double dt, const unsigned int T)
  {
    // No C++ in here, but namespaces work in external C linkage
    // But only from C++ -> C direction, don't try to define new namespaces inside this C realm
    Backend::simulate(x, v, N, dim, dt, T);
  }
}
