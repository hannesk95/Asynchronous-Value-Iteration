#include "Iterator.h"

// Interface C code for CFFI
extern "C"
{
    extern void cffi_iterate(double* data, int* indices, int* indptr, const unsigned int n_rows,
                             const unsigned int n_columns, double* J_star, double* J, double* pi, double epsilon,
                             double alpha, const unsigned int n_actions, const unsigned int n_stars,
                             const unsigned int n_states, const unsigned int n_nonzero)
    {
        Backend::iterate(data, indices, indptr, n_rows, n_columns, J_star, J, pi, epsilon, alpha, n_actions,
                         n_stars, n_states, n_nonzero);
    }
}
