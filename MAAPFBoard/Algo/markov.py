EPSILON = 0.01


class MDP:

    """A Markov Decision Process, defined by an states, actions, transition model and reward function."""

    def __init__(self, graph, reward, gamma):
        self._states = graph
        self._reward = reward
        self._gamma = gamma

    def reward(self, state):
        """return reward for this state."""
        return self._reward(state)

    def value_iteration(self):
        value_dict = {s: 0 for s in self._states}

        while delta > EPSILON:
            prev_value_dict = value_dict.copy()
            delta = 0
            for s in self._states:
                route_sum = []
                for state in self._states:
                    route_sum.append([pr * value_dict[node] for (node, pr) in zip(state.vertices, state.pr)])
                value_dict[s] = self.reward(s) + self.gamma * max(route_sum)
                delta = max(delta, abs(value_dict[s] - prev_value_dict[s]))
        return value_dict
