from Algo.mdp import MDP
from typing import List, Dict, Tuple, Iterator
import Algo.dijkstra as heru 
import time
import random

class RTDP(MDP):

    def __init__(self, graph):
        super().__init__(graph, "RTDP")
        self.table_delta = {}
        self.policy_delta = {}
        self._visit_table = {}
        self._empty = '$'

    @property
    def visit_table(self):
        return self._visit_table

    def _r_q_value(self, next_step, heuristic, target, sink_reward=-200):
        calc = []
        if self.table[next_step][-1] == self._empty:
            h_val = 0
            for s, t in zip(next_step, target):
                h_val += heuristic(self._graph, s, t)
            self._table[next_step] = [h_val]
        for m in next_step:
            calc.append(
                ((1 - self._graph.prob[m]) * self._table[next_step][-1]) + (self._graph.prob[m] * sink_reward))
        return -1 + sum(calc)

    def _greedy_action(self, state, heuristic, target):
        actions = self._get_actions(state)
        q_values = [self._r_q_value(ns, heuristic, target) for ns in actions]
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

    def _trial(self, start, target, heuristic):
        start_min = time.localtime().tm_min
        curr_state = start
        path = [curr_state]
        while curr_state != target:

            for np in curr_state:
                self.visit_table[np] += 1
            action = self._greedy_action(curr_state, heuristic, target)
            self.table[curr_state].append(self._r_q_value(action, heuristic, target))
            if len(self.table[curr_state]) > 20:
                self.table[curr_state].pop(0)

            next_state = self._next_state(curr_state, action)
            if not next_state:
                break

            curr_state = next_state
            path.append(next_state)
            end_min = time.localtime().tm_min
            if end_min < start_min:
                end_min += 60
            if end_min - start_min > 5:
                break

        if curr_state == target:
            for np in curr_state:
                self.visit_table[np] += 1
            # print("found path")
            # print(path)

    def rtdp(self, start, target, limit=None, delta=0.00001, delta_limit=20, heuristic=heru.h_len):
        start_min = time.localtime().tm_min
        self._init_table(len(target))

        for state in self._table:
            self._table[state].append(self._empty)

        self._table[target] = [30]
        for p in self._graph.prob:
            self.visit_table[p] = 0
        iter_limit = limit if limit else 200000
        stop = 0
        for i in range(iter_limit):
            self._trial(start, target, heuristic)
            stop = stop + 1 if self._check_delta(delta) else 0
            end_min = time.localtime().tm_min
            if end_min < start_min:
                end_min += 60
            if end_min - start_min > 5:
                print("fail to finish in 5 minutes")
                break
            if i > 500 and stop > delta_limit:
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

