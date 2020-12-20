#ifndef _SIMULATOR_H_
#define _SIMULATOR_H_

#define EIGEN_USE_BLAS
#define EIGEN_USE_LAPACKE
#include "Eigen/Dense"
#include "Eigen/Sparse"

namespace Backend
{
  void iterate(Eigen::Ref<Eigen::SparseMatrix<double, Eigen::RowMajor>> t_prob_matrix,
               Eigen::Ref<Eigen::VectorXd> opt_state_values, Eigen::Ref<Eigen::VectorXd> state_val_buf,
               Eigen::Ref<Eigen::VectorXd> policy_val_buf, double epsilon, double alpha, const unsigned int n_actions,
               const unsigned int n_stars, const unsigned int n_states);

  void iterate(double* data, int* indices, int* indptr, const unsigned int n_rows,
               const unsigned int n_columns, double* J_star, double* J, double* pi, double epsilon,
               double alpha, const unsigned int n_actions, const unsigned int n_stars, const unsigned int n_states);
}

#endif
