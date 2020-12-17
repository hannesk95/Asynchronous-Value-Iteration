import pickle
import logging

logger = logging.getLogger(__name__)

import numpy as np
import scipy.sparse
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import graphsearch

#---------------------------------------------------------------------------------------

def state_to_tuple(x, n_stars):
  # Fuel f, goal star g and current node in graph i
  f = x // (n_stars * n_stars)
  g = x % (n_stars * n_stars) // n_stars
  i = x % (n_stars * n_stars) % n_stars

  return f, g, i

def state_from_tuple(f, g, i, n_stars):
  """ Fuel f, goal star g and current node in graph i """
  return f * n_stars * n_stars + g * n_stars + i

def jump(x, u, P, max_u):
  targets = P[x * max_u + u].nonzero()[1]

  if targets.size == 0:
    raise ValueError(f"Control {u=} is not allowed in state {x=}")

  disturbance = np.random.randint(0, targets.size)

  return targets[disturbance]

def travel(state, P, policy, n_stars, max_u, max_len=250):
  f, g, i = state_to_tuple(state, n_stars)

  path = [i]
  cur = state
  goal_reached = False

  while not goal_reached and len(path) < max_len:
    cur = jump(cur, policy[cur], P, max_u)

    _, _, i = state_to_tuple(cur, n_stars)

    goal_reached = i == g

    path.append(i)

  return path

def path_to_coor(path, stars):
  return np.array([stars[node, :] for node in path])

def plot_full_graph(adjacency, coordinates, star_types, *paths):

  connections_from = []
  connections_to = []

  for i, j in zip(*adjacency.nonzero()):
    connections_from.append(coordinates[i, :])
    connections_to.append(coordinates[j, :] - coordinates[i, :])

  connections_from = np.array(connections_from)
  connections_to = np.array(connections_to)

  plt.figure()

  plt.quiver(connections_from[:, 0], connections_from[:, 1], connections_to[:, 0], connections_to[:, 1],
             color='grey', headwidth=1, headlength=0, linewidth=0.5, width=0.001,
             scale_units='xy', scale=1.0, angles='xy')


  for i, path_col in enumerate(paths):

    if type(path_col) == tuple:
      path, color = path_col
    else:
      path, color = path_col, "orange"

    if path is None:
      print("Skipping invalid path -> no connection from start to goal")
      continue

    start = path[0]
    goal = path[-1]
    path_coor = path_to_coor(path, coordinates)

    plt.plot(coordinates[start, 0], coordinates[start, 1], 'x', color=color)
    plt.plot(coordinates[goal, 0], coordinates[goal, 1], 'x', color=color)
    plt.plot(path_coor[:, 0], path_coor[:, 1], '-o', linewidth=3.0, color=color)

    plt.annotate(f"start {i}",
                 xy=coordinates[start, :], xycoords='data',
                 xytext=(10, 10), textcoords='offset points',
                 color="k",
                 arrowprops={'arrowstyle': '->', 'color': "k"})
    plt.annotate(f"end {i}",
                 xy=coordinates[goal, :], xycoords='data',
                 xytext=(10, 10), textcoords='offset points',
                 color="k",
                 arrowprops={'arrowstyle': '->', 'color': "k"})

  fuel_stars = coordinates[np.argwhere(star_types > 0).squeeze()]
  normal_stars = coordinates[np.argwhere(star_types < 1).squeeze()]

  plt.plot(fuel_stars[:, 0], fuel_stars[:, 1], 'o', color="blue")
  plt.plot(normal_stars[:, 0], normal_stars[:, 1], '.', color="blue")

  plt.grid()
  plt.xlabel("x")
  plt.ylabel("y")

  return

def plot_graph_part(start_node, max_depth, adjacency, coordinates, path=None, confusion_distance=None):
  node_transitions = []

  queue = [(start_node, 0)]

  while len(queue) > 0:
    cur, depth = queue.pop(0)

    if depth >= max_depth:
      continue

    # All successors: Non-zero entries of current row, pick columns by [1]
    # Self loops are not in graph!
    for nxt in adjacency[cur].nonzero()[1]:
      node_transitions.append((cur, nxt))
      queue.append((nxt, depth + 1))

  connections_from = []
  connections_to = []

  nodes_to_draw = set()

  for i, j in node_transitions:
    nodes_to_draw.add(i)
    nodes_to_draw.add(j)

    connections_from.append(coordinates[i, :])
    connections_to.append(coordinates[j, :] - coordinates[i, :])
  # end

  connections_from = np.array(connections_from)
  connections_to = np.array(connections_to)
  nodes_to_draw = np.array(list(nodes_to_draw))

  plt.figure()

  if len(connections_from) == 0 or len(connections_to) == 0:
    logger.warning("Disconnected graph for the current node")
  else:
    plt.quiver(connections_from[:, 0], connections_from[:, 1], connections_to[:, 0], connections_to[:, 1],
               color='grey', headwidth=1, headlength=0, linewidth=0.5, width=0.001,
               scale_units='xy', scale=1.0, angles='xy')

    plt.plot(coordinates[nodes_to_draw, 0], coordinates[nodes_to_draw, 1], '.', color="blue")

  if confusion_distance is not None:
    ax = plt.gca()

    for node in nodes_to_draw:
      ax.add_artist(plt.Circle(coordinates[node, :], confusion_distance,
                               ec="grey", ls=":", fill=False))

  if path is not None:
    path_coor = np.array([coordinates[node, :] for node in path])
    plt.plot(path_coor[:, 0], path_coor[:, 1], '-o', linewidth=3.0, color="orange")

  plt.annotate("origin",
               xy=coordinates[start_node, :], xycoords='data',
               xytext=(10, 10), textcoords='offset points',
               color="red",
               arrowprops={'arrowstyle': '->', 'color': "red"})

  plt.grid()
  plt.xlabel("x")
  plt.ylabel("y")

  return

def load_sparse_matrix(data_dir, name):
  indptr = np.load(f"{data_dir}/{name}_indptr.npy")
  indices = np.load(f"{data_dir}/{name}_indices.npy")
  data = np.load(f"{data_dir}/{name}_data.npy")
  shape = np.load(f"{data_dir}/{name}_shape.npy")
  return data, indices, indptr, shape

def to_sparse_matrix(data, indices, indptr, shape):
  # Eigen provides a similar why to create a CSR view of these arrays, take a look at Eigen::Map< CSR Matrix >(...)
  return scipy.sparse.csr_matrix((data, indices, indptr), shape=shape, dtype=data.dtype)

def one_step_cost(state, control, n_stars):
  f, g, i = state_to_tuple(state, n_stars)

  # In goal and no jump
  if g == i and control == 0:
    return -100.0

  # Out of fuel
  if f == 0:
    return 100.0

  # Avoid unnecessary jumps
  if control > 0:
    return 5.0

  # Else no cost
  return 0.0

#---------------------------------------------------------------------------------------

# data_dir = "data_normal"
# data_dir = "data_small"
data_dir = "data_debug"

P = to_sparse_matrix(*load_sparse_matrix(data_dir, "P"))  # True transition probs
p = P.toarray() #convert sparse matrix to dense matrix

star_graph = to_sparse_matrix(*load_sparse_matrix(data_dir, "star_graph"))  # the mere radius neighbor graph (sklearn)

stars = np.load(f"{data_dir}/stars.npy")  # Coordinates of stars
star_types = np.load(f"{data_dir}/star_types.npy")  # Fuel star or not as lookup table (mostly for rendering)

J_star = np.load(f"{data_dir}/J_star_alpha_0_99_iter_1000.npy")  # Reference solution
pi_star = np.load(f"{data_dir}/pi_star_alpha_0_99_iter_1000.npy")  # Corresponding optimal policy

with open(f"{data_dir}/parameters.pickle", "rb") as the_file:
  parameters = pickle.load(the_file)

max_u = parameters["max_controls"]
n_stars = parameters["number_stars"]
max_f = parameters["fuel_capacity"]

#---------------------------------------------------------------------------------------

some_state = state_from_tuple(max_f - 1,  # Start with max fuel
                              n_stars - 1,  # Goal is last star
                              0,  # Start is the star with label 0
                              n_stars)

fuel, goal_star, cur_star = state_to_tuple(some_state, n_stars)
cost = one_step_cost(some_state, 2, n_stars)

# Some paths through the graph
path = graphsearch.a_star(cur_star, goal_star, star_graph, stars)
path2 = travel(some_state, P, pi_star, n_stars, max_u)

plot_full_graph(star_graph, stars, star_types, (path, "green"), (path2, "red"))

plot_graph_part(start_node=cur_star,
                max_depth=2,  # All raw graph edges, two hops from current star
                adjacency=star_graph, coordinates=stars,
                confusion_distance=parameters["confusion_distance"])
plt.show()

print("Current star:", cur_star)
print("Its direct successors according to 'raw' graph:")

# Nonzero returns array with row indices and array with col indices
for j in star_graph[cur_star].nonzero()[1]:
  print(f"  Star {j} at position {stars[j, :]}")

print()
print("All available transitions for the current star:")

# The loop goes over all possible values -> there is at least one star with max_U outgoing jumps, the rest has less
for u in range(max_u):

  # State is Major Row Index, per state there are max_U "subrows"
  row_in_P = some_state * max_u + u

  # Fetch the non-zero transitions for state 'some_state' and the control u
  non_zero_transitions = P[row_in_P, :].nonzero()[1]

  # This loop won't run if u is not valid -> zero row is placeholder == no successor
  for j in non_zero_transitions:
    print(f"  From star {cur_star} with control {u} you can reach state {j} with chance {P[row_in_P, j]}")

  if non_zero_transitions.size == 0:
    print(f"  At star {cur_star} control {u} is not allowed -> zero row in P")
