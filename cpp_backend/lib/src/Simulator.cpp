#include "Simulator.h"
#include <iostream>

#include <Eigen/Sparse>
#include <vector>
#include <omp.h>
#include <tuple>
#include <complex>

namespace Backend
{

    void state_to_tuple(unsigned int state, const unsigned int n_stars, std::tuple<int, int, int> &properties)
    {
        int f = state / (n_stars * n_stars);
        int g = state % (n_stars * n_stars) / n_stars;
        int i = state % (n_stars * n_stars) % n_stars;
        properties = std::make_tuple(f,g,i);
    }

    void one_step_cost(unsigned int state, const unsigned int control, const unsigned int n_stars, float &cost)
    {
        std::tuple<int, int, int> properties;
        state_to_tuple(state, n_stars, properties);

        int f = std::get<0>(properties);
        int g = std::get<1>(properties);
        int i = std::get<2>(properties);

        if (g == i && control == 0)
        {
            cost = -100.0;
        }

        else if (f == 0)
        {
            cost = 100.0;
        }

        else if (control > 0)
        {
            cost = 5.0;
        }
        else
        {
            cost = 0.0;
        }
    }

    void iterate(Eigen::Ref<Eigen::SparseMatrix<double, Eigen::RowMajor>> t_prob_matrix,
                 Eigen::Ref<Eigen::VectorXd> opt_state_values, Eigen::Ref<Eigen::VectorXd> state_val_buf,
                 Eigen::Ref<Eigen::VectorXd> policy_val_buf, double epsilon, double alpha, const unsigned int n_actions,
                 const unsigned int n_stars, const unsigned int n_states)
    {

        // Set number of thread using OpenMP
        omp_set_num_threads(4);

        // Declare error variable
        double error = std::numeric_limits<double>::infinity();

        // Declare sparse matrix which will include slices of original sparse matrix
        Eigen::SparseMatrix<double, Eigen::RowMajor> t_prob_matrix_slice(n_actions, n_states);

        // Declare variable which stores cost
        float cost = 0;

        // Declare vector which stores the values for each actions belonging to a state
        std::vector<float> min_actions(n_actions, 0.0);

        //while(error > epsilon)
        // #pragma omp parallel
        {
            // #pragma omp for
            for (unsigned int iteration = 0; iteration < 1000; iteration++)
            {
                // #pragma omp for
                for (unsigned int state = 0; state < n_states; state++)
                {

                    t_prob_matrix_slice = t_prob_matrix.middleRows(state * n_actions, n_actions);

                    // #pragma omp for
                    for (unsigned int action = 0; action < n_actions; action++)
                    {
                        auto t_prob_vec = t_prob_matrix_slice.innerVector(action);

                        if (t_prob_vec.sum() == 0)
                            continue;

                        one_step_cost(state, action, n_stars, cost);

                        //auto cur_action_cost = t_prob_vec.dot(cost + (alpha * state_val_buf.array()));
                        cost = t_prob_vec.dot((cost + (alpha * state_val_buf).array()).matrix());
                        // auto cur_action_cost = 5;
                        // cur_action_cost = (t_prob_vec.cwiseProduct(cost + (alpha * state_val_buf.array())).matrix()).sum();

                        min_actions.insert(min_actions.begin() + action, cost);
                    }


                    state_val_buf[state] = double(*std::min_element(min_actions.begin(), min_actions.end()));
                    // std::cout << "State: "<< std::min_element(min_actions.begin(), min_actions.end()) - min_actions.begin() << std::endl;
                    policy_val_buf[state] =
                            std::min_element(min_actions.begin(), min_actions.end()) - min_actions.begin();
                    // std::cout << "State: "<< state << std::endl;
                }


                // error = (state_val_buf.norm() - opt_state_values.norm()); // .array().abs();
            }
        }
    }

    void iterate(double* data, int* indices, int* indptr, const unsigned int n_rows,
                 const unsigned int n_columns, double* J_star, double* J, double* pi, double epsilon,
                 double alpha, const unsigned int n_actions, const unsigned int n_stars, const unsigned int n_states)
    {
        // Create sparse matrix by mapping external buffers
        Eigen::Map<Eigen::SparseMatrix<double, Eigen::RowMajor>> t_prob_matrix(n_rows, n_columns, 290,
                                                                               indices, indptr, data);
        // Create array in which state values are stored
        Eigen::Map<Eigen::VectorXd> state_val_buf(J, n_states);

        // Create array in which the optimal state values are stored
        Eigen::Map<Eigen::VectorXd> opt_state_values(J_star, n_states);

        // Create array in which the policy is stored
        Eigen::Map<Eigen::VectorXd> policy_val_buf(pi, n_states);

        // Invoke asynchronous value iteration procedure
        iterate(t_prob_matrix, opt_state_values, state_val_buf, policy_val_buf, epsilon, alpha, n_actions, n_stars, n_states);
    }
}
