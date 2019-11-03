from Algo.mdp import MDP
from typing import List, Dict, Tuple, Iterator
from Algo.dijkstra import pron_w as dijkstra
import time
import random


class RTDP(MDP):

    def __init__(self, graph):
        super().__init__(graph, "RTDP")
        self.table_delta = {}
        self.policy_delta = {}
        self.visit_table = {}

    def _greedy_action(self, state):
        actions = self._get_actions(state)
        q_values = [self._q_value(state, ns) for ns in actions]
        max_i = max(range(len(q_values)), key=q_values.__getitem__)
        return actions[max_i]

    def _next_state(self, state, action):
        death_prob = 1
        next_state = None
        for s in action:
            death_prob *= self._graph.prob[s]
        if random.choices([True, False], weights=[1 - death_prob, death_prob])[0]:
            next_state = action
        return next_state

    def _trial(self, start, target):
        start_min = time.localtime().tm_min
        curr_state = start
        path = [curr_state]
        while curr_state != target:
            action = self._greedy_action(curr_state)
            # print(action)
            self.table[curr_state].append(self._q_value(curr_state, action))
            if len(self.table[curr_state]) > 20:
                self.table[curr_state].pop(0)

            next_state = self._next_state(curr_state, action)
            if not next_state:
                break
            curr_state = next_state
            path.append(next_state)
            for np in next_state:
                self.visit_table[np] += 1
            end_min = time.localtime().tm_min
            if end_min < start_min:
                end_min += 60
            if end_min - start_min > 3:
                break
        if curr_state == target:
            print("found path")
            print(path)

    def rtdp(self, start, target, limit=None, delta=0.0001, delta_limit=10, heuristic=dijkstra):
        start_min = time.localtime().tm_min
        self._init_table(len(target))
        dijkstra_vals = [heuristic(self._graph, pos) for pos in target]
        for state in self._table:
            h_state = 0
            for pos, dijkstra_val in zip(state, dijkstra_vals):
                assert pos in dijkstra_val
                h_state += dijkstra_val[pos]
            self._table[state].append(h_state)
        for p in self._graph.prob:
            self.visit_table[p] = 0
        iter_limit = limit if limit else 10000
        stop = 0
        for i in range(iter_limit):
            self._trial(start, target)
            stop = stop + 1 if self._check_delta(delta) else 0
            end_min = time.localtime().tm_min
            if end_min < start_min:
                end_min += 60
            if end_min - start_min > 3:
                print("fail to finish in 5 minutes")
                break
            if stop == delta_limit:
                break
        return i

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

    def _check_policy_delta(self) -> bool:
        """
        check if the latest iteration change is smaller then delta.
        :param delta: the maximal difference between two value iterations.
        :return: True if all the values in the table didn't change more then delta
        """
        stop = False
        if not self.policy_delta:
            self.policy_delta = self.policy
        else:
            stop = self.policy_delta == self.policy
            self.policy_delta = self.policy
        return stop

