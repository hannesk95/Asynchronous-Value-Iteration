import numpy as np
import heapq

def _a_star_heuristic(a, b, X):
  return np.linalg.norm(X[a, :] - X[b, :])

def _a_star_reconstruct_path(cameFrom, current):
  total_path = [current]

  while current in cameFrom.keys():
    current = cameFrom[current]
    total_path = [current] + total_path

  return total_path

def _a_star_neighbours(node, graph):
  return np.argwhere(graph[node, :] > 0.0)[:, 1]

def _a_star_edge_cost(a, b):
  return 1

def a_star(start, goal, graph, X):

  # The set of discovered nodes that need to be (re-)expanded.
  # Initially, only the start node is known.
  openSet = []
  heapq.heappush(openSet, (0, start))

  # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start to n currently known.
  cameFrom = {}

  # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
  gScore = {start: 0}

  # For node n, fScore[n] := gScore[n] + heuristic_cost_estimate(n, goal).
  fScore = {start: _a_star_heuristic(start, goal, X)}

  while openSet:
    priorty, current = heapq.heappop(openSet)

    if current == goal:
      return _a_star_reconstruct_path(cameFrom, current)

    for neighbor in _a_star_neighbours(current, graph):

      # The distance from start to the neighbor through current
      tentative_gScore = gScore.get(current, np.inf) + _a_star_edge_cost(current, neighbor)

      # This path to neighbor is better than any previous one. Record it!
      if tentative_gScore < gScore.get(neighbor, np.inf):
        cameFrom[neighbor] = current
        gScore[neighbor] = tentative_gScore
        fScore[neighbor] = gScore[neighbor] + _a_star_heuristic(neighbor, goal, X)

        exists = any([neighbor == foo[1] for foo in openSet])
        if not exists:
          heapq.heappush(openSet, (fScore[neighbor], neighbor))
        # end
      # end
    # end

  # No path found -> None
  return
