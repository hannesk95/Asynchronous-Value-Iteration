#ifndef _SIMULATOR_H_
#define _SIMULATOR_H_

#define EIGEN_USE_BLAS
#define EIGEN_USE_LAPACKE
#include "Eigen/Dense"

namespace Backend
{

  ///
  /// \brief Gravity between Particle x1 and x2
  /// \param f Eigen::VectorXd which stores the force
  /// \param x1 Eigen::VectorXd with position of particle 1
  /// \param x2 Eigen::VectorXd with position of particle 1
  ///
  /// This calculates the gravity between two particles with equal weight
  /// The force is calculated from the viewpoint of particle one, i.e. the
  /// first particle receives f, the second -f.
  void force(Eigen::Ref<Eigen::VectorXd> f, const Eigen::Ref<const Eigen::VectorXd>& x1, const Eigen::Ref<const Eigen::VectorXd>& x2);

  ///
  /// \brief A single Eulerstep to advance the particle simulation by dt seconds
  /// \param x Eigen::MatrixXd with all positions, each column is one particle
  /// \param v Eigen::MatrixXd with all velocities, each column is one particle
  /// \param dt Elapsed time between two steps
  ///
  /// Calculates a single Euler step for the particle simulation.
  ///
  void simulate(Eigen::Ref<Eigen::MatrixXd> x, Eigen::Ref<Eigen::MatrixXd> v, const double dt);

  ///
  /// \brief T steps for the simulation
  /// \param x Eigen::MatrixXd with all positions, each column is one particle
  /// \param v Eigen::MatrixXd with all velocities, each column is one particle
  /// \param dt Elapsed time between two steps
  /// \param T number of steps
  ///
  ///  Calls T times Backend::simulate(Eigen::Ref<Eigen::MatrixXd>, Eigen::Ref<Eigen::MatrixXd>,const double) to advance the simulation by T * dt seconds.
  ///
  ///  \overload
  ///
  void simulate(Eigen::Ref<Eigen::MatrixXd> x, Eigen::Ref<Eigen::MatrixXd> v,
                const double dt, const unsigned int T);

  ///
  /// \brief Cffi wrapper for Backend::simulate()
  /// \param x continuous memory of all positions
  /// \param v continuous memory of all velocities
  /// \param N number of particles, i.e. number of columns
  /// \param dim dimension of the dynamical system, i.e. number of rows
  /// \param dt Elapsed time between two steps
  ///
  /// Converts the continous memory to Eigen::MatrixXd and calls the basic Backend::simulate(Eigen::Ref<Eigen::MatrixXd>, Eigen::Ref<Eigen::MatrixXd>,const double).
  /// For use with CFFI.
  ///
  /// \overload
  ///
  void simulate(double* x, double* v,
                const unsigned int N, const unsigned int dim,
                const double dt);

  ///
  /// \brief Cffi wrapper for Backend::simulate() to advance the simulation T steps
  /// \param x continuous memory of all positions
  /// \param v continuous memory of all velocities
  /// \param N number of particles, i.e. number of columns
  /// \param dim dimension of the dynamical system, i.e. number of rows
  /// \param dt Elapsed time between two steps
  /// \param T number of steps
  ///
  /// Converts the continous memory to Eigen::MatrixXd and calls the basic Backend::simulate(Eigen::Ref<Eigen::MatrixXd>, Eigen::Ref<Eigen::MatrixXd>, const double, const unsigned int) to advance the simulation by T * dt seconds.
  /// For use with CFFI.
  ///
  /// \overload
  ///
  void simulate(double* x, double* v,
                const unsigned int N, const unsigned int dim,
                const double dt, const unsigned int T);
}

#endif
