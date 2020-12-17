#include <iostream>
#include <cmath>
#include <chrono>
#include "omp.h"
#include "Definitions.h"
#include "Simulator.h"
#include <Eigen/Sparse>

int main(int argc, char *argv[])
{

  Eigen::SparseMatrix<double> A(600, 125);
  std::cout << "Shape: " << A.innerSize() << std::endl;

  Eigen::MatrixXd x(2, 3);
  x << 0.0, 1.0, -1.0,
       0.0, 1.0, -1.0;

  Eigen::MatrixXd v(2, 3);
  v.fill(0.0);

  std::cout << "Before step" << std::endl;
  std::cout << "x:" << std::endl << x << std::endl;
  std::cout << "v:" << std::endl << v << std::endl;

  auto t0 = std::chrono::system_clock::now();

  Backend::simulate(x, v, 0.1);

  auto t1 = std::chrono::system_clock::now();

  std::cout << "After step" << std::endl;
  std::cout << "x:" << std::endl << x << std::endl;
  std::cout << "v:" << std::endl << v << std::endl;


  std::cout
    << "This took "
    << std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count()
    << " micro seconds" << std::endl;

  return 0;
}
