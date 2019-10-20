from Algo.mdp import MDP
from typing import List, Dict, Tuple, Iterator
from Algo.dijkstra import pron_w as dijkstra


class RTDP(MDP):

    def __init__(self, graph):
        super().__init__(graph)
        self.table_delta = {}

    def _greedy_action(self, state):
        actions = self._get_actions(state)
        min_action = [actions[0], self._q_value(state, actions[0])]
        actions.pop(0)
        for next_step in actions:
            val = self._q_value(state, next_step)
            if val > min_action[1]:
                min_action[0] = next_step
                min_action[1] = val
        return min_action[0]

    def _next_state(self, state, action):
        return action

    def _q_value(self, state, next_step):
        calc = []
        sink_reward = -100
        for c, m in zip(state, next_step):
            # if c != m:
            calc.append(
                ((1 - self._graph.prob[m]) * self._table[next_step][-1]) + (self._graph.prob[m] * sink_reward))
        return -1 + sum(calc)

    def _trial(self, start, target):
        curr_state = start
        while curr_state != target:
            action = self._greedy_action(curr_state)
            self.table[curr_state].append(self._q_value(curr_state, action))
            curr_state = self._next_state(curr_state, action)

    def rtdp(self, start, target, limit=None, delta=0.00001, delta_limit=20):
        self._init_table(len(target))
        dijkstra_vals = [dijkstra(self._graph, pos) for pos in target]
        for state in self._table:
            h_state = 0
            for pos, dijkstra_val in zip(state, dijkstra_vals):
                assert pos in dijkstra_val
                h_state += dijkstra_val[pos]
            self._table[state].append(h_state)
        iter_limit = limit if limit else 1000
        stop = 0
        for i in range(iter_limit):
            self._trial(start, target)
            stop = stop + 1 if self._check_delta(delta) else 0
            if stop == delta_limit:
                break

        return -1 if i == iter_limit - 1 else i

    def policy_path(self, source, target):
        path = list()
        self._policy = {}
        curr_state = source
        while curr_state != target:
            path.append(curr_state)
            action = self._greedy_action(curr_state)
            self._policy[curr_state] = [action]
            curr_state = self._next_state(curr_state, action)
        path.append(curr_state)
        return path

    def _check_delta(self, delta: float) -> bool:
        """
        check if the latest iteration change is smaller then delta.
        :param delta: the maximal difference between two value iterations.
        :return: True if all the values in the table didn't change more then delta
        """
        stop = False
        for pos, row in self.table.items():
            if pos in self.table_delta:
                old_val = self.table_delta[pos]
                new_val = len(row)
                self.table_delta[pos] = new_val
                if old_val < new_val and abs(row[-1] - row[-2]) > delta:
                    break
            else:
                self.table_delta[pos] = len(row)
        else:
            stop = True
        return stop
