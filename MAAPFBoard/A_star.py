class MAAPFAlgorithms:
    """collections of A* based algorithms."""

    def __init__(self, heuristic_func, neighbors_func, dist_func):
        self.heuristic_func = heuristic_func
        self.neighbors_func = neighbors_func
        self.dist_func = dist_func

    def a_star(self, start, goal):
        """A simple implementation of the basic version of A* path finding algorithm."""
        closed_set = set()  # The set of nodes already evaluated.
        open_set = set()  # The set of tentative nodes to be evaluated, initially containing the start node
        came_from = dict()  # The map of navigated nodes.

        g_score = dict()
        f_score = dict()

        open_set.add(start)
        g_score[start] = 0  # Cost from start along best known path.
        # Estimated total cost from start to goal through y.
        f_score[start] = g_score[start] + self.heuristic_cost_estimate(start, goal)

        while open_set:
            current = self.__get_min_val(open_set, f_score)  # the node in openset having the lowest f_score[] value
            if current == goal:
                return self.__reconstruct_path(came_from, goal)

            open_set.remove(current)
            closed_set.add(current)
            for neighbor in self.neighbor_nodes(current):
                tentative_g_score = g_score[current] + self.dist_between_nodes(current, neighbor)
                if (neighbor in closed_set
                        or (neighbor in g_score and tentative_g_score >= g_score[neighbor])):
                    continue

                if (neighbor not in open_set
                        or (neighbor in g_score and tentative_g_score < g_score[neighbor])):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic_cost_estimate(neighbor, goal)
                    open_set.add(neighbor)

        return None

    def __reconstruct_path(self, came_from, current_node):
        res_node = current_node
        if current_node in came_from:
            p = self.__reconstruct_path(came_from, came_from[current_node])
            return str(p) + ' -> ' + str(current_node)
        return res_node

    def heuristic_cost_estimate(self, s, t):
        """An estimated distance from node s to node t."""
        return self.heuristic_func(s, t)

    def dist_between_nodes(self, s, t):
        """return the distance (weights) between two neighbors nodes."""
        return self.dist_func(s, t)

    def neighbor_nodes(self, node):
        """return all the neighbor nodes of a node in the graph, None if not found."""
        return self.neighbors_func(node)

    @staticmethod
    def __get_min_val(set_e: set, dict_v: dict):
        """return the element in set_e with the lowest value in dict_v."""
        return min([(k, v) for k, v in dict_v.items() if k in set_e], key=lambda t: t[0])[0]
