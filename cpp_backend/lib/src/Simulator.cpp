#include "Simulator.h"
#include "Definitions.h"
#include <iostream>

#include <Eigen/Sparse>
#include <vector>

namespace Backend
{
  void force(Eigen::Ref<Eigen::VectorXd> f, const Eigen::Ref<const Eigen::VectorXd> &x1, const Eigen::Ref<const Eigen::VectorXd> &x2)
  {
    // Connecting vector from particle one to particle 2, the reference can be used as target for the operation
    f = x2 - x1;

    // Euclidean distance of the two particles
    double r = f.norm();

    // Now normalize the connection vector to just have a unit direction
    f /= r;

    // Combine both into the gravity that is acting on particle 1
    f *= GRAVITY_CONSTANT * PARTICLE_MASS * PARTICLE_MASS / (r * r);
  }

  void simulate(Eigen::Ref<Eigen::MatrixXd> x, Eigen::Ref<Eigen::MatrixXd> v, const double dt)
  {
    const unsigned int N = x.cols(), dim = x.rows();

    static Eigen::MatrixXd F(dim, N);  // Static to keep storage alive
    F.fill(0.0);                       // -> Remove values from last round

    Eigen::VectorXd f(dim);

    // Try to parallelize this loop, but pay attention to asynchronous writing of F -> mutex  required
    for (unsigned int p1 = 0; p1 < N; p1++)
    {
      // This one is easier, but the workload shrinks with increasing p1
      for (unsigned int p2 = p1 + 1; p2 < N; p2++)
      {
        force(f, x.col(p1), x.col(p2));

        F.col(p1) += f;
        F.col(p2) -= f;
      }
    }

    // Simple euler step
    v = VELOCITY_DAMPENING * v + dt * F / PARTICLE_MASS;
    v = v.array().min(V_MAX).max(-V_MAX);  // Clipping, since euler integration is not the best

    x = x + dt * v;
    x = x.array().min(X_MAX).max(-X_MAX);  // Clipping, since euler integration is not the best
  }
  void simulate(Eigen::Ref<Eigen::MatrixXd> x, Eigen::Ref<Eigen::MatrixXd> v,
                const double dt, const unsigned int T)
  {
    for (unsigned int t = 0; t < T; t++) simulate(x, v, dt);
  }

  void simulate(double* x, double* v, const unsigned int N, const unsigned int dim, const double dt)
  {
    // Don't use a row major format here: the continuous data from outside comes from row major format
    // and must be written transposed in col major matrix, such that each col of x or v is one row of
    // the original numpy array
    Eigen::Map<Eigen::MatrixXd> x_map(x, dim, N), v_map(v, dim, N);

    simulate(x_map, v_map, dt);
  }

  void simulate(double* x, double* v,
                const unsigned int N, const unsigned int dim,
                const double dt, const unsigned int T)
  {
    // Don't use a row major format here: the continuous data from outside comes from row major format
    // and must be written transposed in col major matirx, such that each col of x or v is one row of
    // the original numpy array
    Eigen::Map<Eigen::MatrixXd> x_map(x, dim, N), v_map(v, dim, N);

    simulate(x_map, v_map, dt, T);
  }

  // template<typename Derived>
  void iterate(const Eigen::SparseMatrix<double> &sparse_matrix, vector<double> &J_star)
  {
    for(unsigned int iteration = 0; iteration < 1000; iteration++)
    {
        for(unsigned int state = 0; state < sparse_matrix.outerSize())
        {
            for(unsigned int action = 0; )
        }
    }

  }

  void iterate(double* t_prob, double* J_star, double* epsilon,
               double* alpha, double* max_u, double* n_stars, double* max_f)
  {
    Eigen::SparseMatrix<double> A(600, 125);
    // vector<double> J(125, 0);
    // vector<double> pi(125, 0);

    //double error = std::numeric_limits<double>::infinity();

  }
}
